# Chatzy AI - Document Verification System

## **Project Overview**

The Chatzy AI Document Verification System is an **intelligent backend system** designed to simulate a real-world **KYC workflow**. It automates the verification of a person's identity by processing multiple document types, extracting structured data, and cross-verifying information for accuracy.

The system performs:

* **Multimodal Data Extraction** from document images (Government ID, Bank Statement, Employment Letter) using Google Gemini 1.5 Flash.
* **Data Normalization** for dates, phone numbers, and addresses.
* **Cross-Document Verification** using 7 validation rules (Name, DOB, Address, Phone, Father's Name, PAN/Aadhaar).
* **Output Generation** to produce a final JSON file with verification results.

---

## **System Process Explained**

The system follows a **5-step pipeline** for each person:

### **1. OCR with Gemini (`ocr.py`)**

* **Purpose:** Extract raw text from document images.
* **How it works:**

  1. The system sends the image to the Gemini API.
  2. Gemini returns raw text as a string.
  3. This text may contain OCR errors like `O ↔ 0` or `l ↔ 1`.
* **Why:** Gemini acts as a highly accurate, cost-effective OCR engine compared to Tesseract or other paid OCR services.

---

### **2. Text Pre-processing (`preprocess.py`)**

* **Purpose:** Clean the raw OCR text before feeding it to the LLM.
* **How it works:**

  * Uses regex patterns to fix common misreads (e.g., numbers, special characters).
  * Simplifies the text, reducing the load on the LLM for structured extraction.

---

### **3. LLM-based Structured Extraction (`llm_extraction.py`)**

* **Purpose:** Convert unstructured text into a **clean JSON with extracted entities**.
* **How it works:**

  1. The cleaned text is sent to Gemini again with a **context-aware prompt** specifying the document type.
  2. Gemini identifies and extracts entities like Name, DOB, PAN, Address, Phone, and Father’s Name.
  3. Returns a **JSON output** ready for normalization.
* **Why:** This replaces complex regex parsing and handles variations intelligently (e.g., multiple date formats or misspelled field labels).

---

### **4. Data Normalization (`normalization.py`)**

* **Purpose:** Standardize data to ensure **accurate cross-document comparisons**.
* **How it works:**

  * **Dates:** Convert all formats to `DD-MM-YYYY`.
  * **Phone Numbers:** Standardize to `+91XXXXXXXXXX`.
  * **Addresses:** Break down into components like pincode, city, and house number for better matching.

---

### **5. Verification & Output (`verification.py`, `app.py`)**

* **Purpose:** Compare extracted and normalized data across the three documents using **7 rules**.
* **Rules include:**

  1. Name consistency
  2. Date of Birth match
  3. Address match
  4. Phone number match
  5. Father's name consistency
  6. PAN format validation
  7. Aadhaar format validation
* **How it works:**

  * Each rule returns `PASS` or `FAIL`.
  * The final status is **VERIFIED** if all critical rules pass, otherwise **FAILED**.
  * Results are saved in `output_all_persons.json` for batch processing or shown on the web interface for single-person testing.

---

## **Key Features**

* **Multimodal Extraction:** OCR + structured extraction with Gemini 1.5 Flash.
* **Intelligent Error Handling:** Corrects common OCR errors automatically.
* **Robust Normalization:** Standardizes dates, phone numbers, and addresses.
* **Comprehensive Verification:** Implements all 7 cross-document rules.
* **Flask API:** Interactive `/process_single` and batch `/process_all` endpoints.
* **Structured Logging:** Logs events in `doc_verification.log` for easy debugging.

---

## **Tech Stack**

* **Backend:** Python, Flask
* **LLM/OCR:** Google Gemini 1.5 Flash
* **Data Processing:** Regex, datetime, JSON
* **Frontend:** HTML, Bootstrap (for single-person testing)
* **Logging:** Python `logging` module

---

## **Project Structure**

```
Document Verification System/
│
├── app.py # Main Flask application orchestrating the full verification flow
├── config.py # Configuration file (API keys, environment variables)
├── output_all_persons.json # Final output file with all extracted and verified results
├── doc_verification.log # Structured logging for debugging and traceability
├── requirements.txt # Python dependencies
|
├── output_all_persons.json # ✅ Final structured output file generated in the root directory
│
├── templates/ # HTML templates for Flask
│ ├── index.html # Web interface for single-person verification
│ └── results.html # Displays structured JSON results
│
├── modules/ # Core logic modules
│ ├── ocr.py # Handles OCR extraction using Google Gemini
│ ├── preprocess.py # Cleans and pre-processes extracted text
│ ├── llm_extraction.py # Structured data extraction using Gemini LLM
│ ├── normalization.py # Normalizes date, phone, and address formats
│ ├── verification.py # Contains 7 rule-based cross-verification checks
│ └── storage.py # Helper utilities (optional)
│
└── dataset/ # Provided input data for testing (10 persons' documents)
    ├── P001/
    ├── P002/
    ├── ...
    └── P010/
```

---

### **📄 Output File Explanation (`output_all_persons.json`)**
This file is automatically generated in the **root directory** after successful execution of `/process_all` or `/process_single` routes.  
It contains structured verification results for each person in the following format:

```
{
  "person_id": "P001",
  "extracted_data": {
    "document_1": { /* extracted fields */ },
    "document_2": { /* extracted fields */ },
    "document_3": { /* extracted fields */ }
  },
  "verification_results": {
    "rule_1_name_match": { "status": "PASS" },
    "rule_2_dob_match": { "status": "PASS" },
    "rule_3_address_match": { "status": "FAIL" },
    "rule_4_phone_match": { "status": "PASS" },
    "rule_5_father_name_match": { "status": "PASS" },
    "rule_6_pan_format": { "status": "PASS" },
    "rule_7_aadhaar_format": { "status": "PASS" }
  },
  "overall_status": "VERIFIED"
}
```
---

### Note:

* Each rule evaluates a specific verification criterion.
* The overall_status is marked as VERIFIED only if all mandatory rules pass; otherwise, it is marked FAILED.
* This JSON serves as the final deliverable for the assignment.

---

## **Installation & Running Locally**

### **1. Clone Repository**

```bash
git clone https://github.com/Sailajayadav/Document-Verification-System.git
cd Document-Verification-System
```

### **2. Create & Activate Virtual Environment**

```bash
python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows
```

### **3. Install Dependencies**

```bash
pip install -r requirements.txt
```

### **4. Add Environment Variables**
Create a .env file and store your Gemini API key
```
GEMINI_API_KEY=your_api_key_here
```

### **5. Run Flask Server**

```bash
python app.py
```

* Batch processing: [http://127.0.0.1:5000/process_all](http://127.0.0.1:5000/process_all)
* Single-person test: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

### Challenges & Solutions

* OCR Accuracy vs Cost: Gemini 1.5 Flash replaced unreliable Tesseract and costly APIs.

* Unstructured Address Matching: Component-based comparison (pincode, city, house number).

* Data Normalization: Dedicated functions unify different date and phone formats.


