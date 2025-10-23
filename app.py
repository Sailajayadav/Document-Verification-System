import os
import logging
from flask import Flask, request, jsonify, send_file, render_template
from modules.ocr import extract_text_from_image
from modules.llm_extraction import extract_entities
from modules.verification import verify_documents
from modules.normalization import normalize_data
from modules.preprocess import preprocess_text
from modules.storage import save_json
import config
import time

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "uploads"
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

logging.basicConfig(
    filename='doc_verification.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_all')
def process_all_persons():
    folder_path = 'dataset'
    all_outputs = []
    expected_docs = {"government_id", "bank_statement", "employment_letter"}
    for person_id in sorted(os.listdir(folder_path)):
        person_folder = os.path.join(folder_path, person_id)
        if not os.path.isdir(person_folder):
            continue
        doc_files = {doc_type: os.path.join(person_folder, f"{person_id}_{doc_type}.png") 
                     for doc_type in expected_docs}
        missing_docs = [doc for doc in expected_docs if not os.path.exists(doc_files[doc])]
        if missing_docs:
            logging.warning(f"Skipping {person_id}: Missing documents {missing_docs}")
            continue
        logging.info(f"Processing {person_id}")
        doc_texts = {}
        for doc_type, path in doc_files.items():
            text = extract_text_from_image(path)
            if text:
                doc_texts[f"document_{list(expected_docs).index(doc_type) + 1}"] = preprocess_text(text)
            else:
                doc_texts[f"document_{list(expected_docs).index(doc_type) + 1}"] = ""
                logging.warning(f"No text extracted for {doc_type} in {person_id}")
        extracted_data = {k: extract_entities(v, k.split("_")[0]) for k, v in doc_texts.items()}
        normalized_data = normalize_data(extracted_data)
        verification_results, overall_status = verify_documents(normalized_data)
        person_output = {
            "person_id": person_id,
            "extracted_data": normalized_data,
            "verification_results": verification_results,
            "overall_status": overall_status
        }
        all_outputs.append(person_output)
        logging.info(f"Completed processing {person_id}")
    output_file = os.path.join(app.root_path, 'output_all_persons.json')
    save_json(all_outputs, output_file)
    return send_file(output_file, as_attachment=True)

@app.route('/process_single', methods=['POST'])
def process_single_person():
    person_id = request.form.get('person_id')
    if not person_id:
        return jsonify({"error": "person_id is required"}), 400
    uploaded_files = request.files.getlist("documents")
    if len(uploaded_files) != 3:
        return jsonify({"error": "Please upload exactly 3 documents"}), 400
    logging.info(f"Processing single person {person_id}")
    doc_texts = {}
    doc_types = ["government_id", "bank_statement", "employment_letter"]
    for i, file in enumerate(uploaded_files, 1):
        if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            return jsonify({"error": "Invalid file type"}), 400
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        time.sleep(1)  # Simulate processing delay
        text = extract_text_from_image(file_path)
        if text:
            doc_texts[f"document_{i}"] = preprocess_text(text)
        else:
            doc_texts[f"document_{i}"] = ""
            logging.warning(f"No text extracted for document_{i} in {person_id}")
        os.remove(file_path)  # Cleanup
    extracted_data = {k: extract_entities(v, doc_types[i-1]) for i, (k, v) in enumerate(doc_texts.items(), 1)}
    normalized_data = normalize_data(extracted_data)
    verification_results, overall_status = verify_documents(normalized_data)
    person_output = {
        "person_id": person_id,
        "extracted_data": normalized_data,
        "verification_results": verification_results,
        "overall_status": overall_status
    }
    return jsonify(person_output)

if __name__ == '__main__':
    app.run(debug=True)