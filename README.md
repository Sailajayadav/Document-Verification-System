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
ChatzyAI/
│
├── app.py                 # Flask server
├── ocr.py                 # OCR module
├── preprocess.py          # Preprocessing OCR text
├── llm_extraction.py      # Structured extraction via Gemini
├── normalization.py       # Standardization of fields
├── verification.py        # Cross-document validation rules
├── templates/
│   └── index.html         # Web UI for single-person testing
├── dataset/               # Input images
├── output_all_persons.json # Final output JSON
└── doc_verification.log   # Logs
```

---

## **Installation & Running Locally**

### **1. Clone Repository**

```bash
git clone <repository_url>
cd ChatzyAI
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

## **Contributors**

* [Amaresh Koneti](https://github.com/amareshkoneti)
