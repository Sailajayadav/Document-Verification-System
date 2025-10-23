import google.generativeai as genai
import json
import re
import logging
from typing import Dict

logger = logging.getLogger(__name__)

def extract_entities(text: str, doc_type: str) -> Dict:
    """
    Use Gemini LLM to extract structured entities from text, handling OCR errors.
    """
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        if doc_type == "employment_letter":
            prompt = f"""
            Extract the following fields from this {doc_type} text, handling OCR errors (e.g., o↔0, l↔1, S↔5) and normalizing formats:
            - Full Name
            - Father's Name
            - Date of Birth (DD-MM-YYYY)
            - Complete Address (house number, street, city, state, pincode)
            - Email Address
            - Aadhaar Number 
            - PAN Number (5 letters + 4 digits + 1 letter)
            - Employee ID
            - Account Number
            Return a valid JSON object with only present fields, e.g., {{"Full Name": "John Doe"}}. If no data is found, return {{}}.
            Text: {text}
            """
        else:
            prompt = f"""
            Extract the following fields from this {doc_type} text, handling OCR errors (e.g., o↔0, l↔1, S↔5) and normalizing formats:
            - Full Name
            - Father's Name
            - Date of Birth (DD-MM-YYYY)
            - Complete Address (house number, street, city, state, pincode)
            - Phone Number (+91XXXXXXXXXX) [Extract only the individual's personal phone number, ignoring organizational contacts]
            - Email Address
            - Aadhaar Number 
            - PAN Number (5 letters + 4 digits + 1 letter)
            - Employee ID
            - Account Number
            Return a valid JSON object with only present fields, e.g., {{"Full Name": "John Doe"}}. If no data is found, return {{}}.
            Text: {text}
            """
        response = model.generate_content(prompt)
        raw_response = response.text
        logger.info(f"Raw LLM response for {doc_type}: {raw_response}")
        
        # Clean the response to extract pure JSON
        json_str = re.sub(r'^```json\n|\n```$', '', raw_response, flags=re.MULTILINE).strip()
        if not json_str:
            logger.warning(f"No valid JSON content in response for {doc_type}")
            return {}
        
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse LLM response as JSON: {str(e)}. Raw response: {raw_response}")
        return {}
    except Exception as e:
        logger.error(f"LLM extraction error: {str(e)}")
        return {}