import re
from datetime import datetime
from typing import Dict, Optional

def normalize_date(date_str: str) -> Optional[str]:
    """Normalize date to DD-MM-YYYY format."""
    formats = ["%d-%m-%Y", "%d/%m/%Y", "%d %b %Y", "%d %B %Y", "%Y-%m-%d", "%d-%m-%y", "%d %B, %Y"]

    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).strftime("%d-%m-%Y")
        except ValueError:
            continue
    return None

def normalize_phone(phone: str) -> Optional[str]:
    """Normalize phone to +91XXXXXXXXXX format."""
    phone = re.sub(r"[^\d]", "", phone)
    if len(phone) == 10:
        return "+91" + phone
    elif len(phone) > 10 and phone.startswith("91"):
        return "+" + phone
    return None

def normalize_address(address: str) -> Dict:
    """Normalize address into components."""
    if not address:
        return {}
    normalized = " ".join(address.split()).replace(",", ", ")
    components = {
        "house_number": "",
        "street": "",
        "city": "",
        "state": "",
        "pincode": ""
    }
    parts = re.split(r",|\s+", normalized)
    for part in parts:
        if re.match(r"^\d{1,4}$", part):
            components["house_number"] = part
        elif re.match(r"^\d{6}$", part):
            components["pincode"] = part
        elif len(part) > 5 and not re.match(r"^\d+", part):
            if not components["city"]:
                components["city"] = part
            elif not components["state"]:
                components["state"] = part
            else:
                components["street"] += " " + part if components["street"] else part
    return components

def normalize_data(extracted_data: Dict) -> Dict:
    """Normalize all extracted data."""
    normalized = {}
    for doc, fields in extracted_data.items():
        doc_norm = fields.copy()
        if fields.get("Date of Birth"):
            doc_norm["Date of Birth"] = normalize_date(fields["Date of Birth"])
        if fields.get("Phone Number"):
            doc_norm["Phone Number"] = normalize_phone(fields["Phone Number"])
        if fields.get("Complete Address"):
            doc_norm["Complete Address"] = normalize_address(fields["Complete Address"])
        normalized[doc] = doc_norm
    return normalized