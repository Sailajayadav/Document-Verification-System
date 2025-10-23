import re
from typing import Dict, Tuple
import logging

logger = logging.getLogger(__name__)

def verify_documents(data: Dict) -> Tuple[Dict, str]:
    results = {}
    overall = "VERIFIED"
    docs = list(data.values())

    # Rule 1: Name matching (already implemented)
    names = [d.get("Full Name", "").lower().strip() for d in docs if d.get("Full Name")]
    normalized_names = [re.sub(r'\s+','', n) for n in names]
    results["rule_1_name_match"] = {"status": "PASS" if len(set(normalized_names)) <= 1 else "FAIL"}
    if results["rule_1_name_match"]["status"] == "FAIL":
        overall = "FAILED"

    # Rule 2: DOB matching
    dobs = [d.get("Date of Birth") for d in docs if d.get("Date of Birth")]
    if dobs and len(set(dobs)) == 1:
        results["rule_2_dob_match"] = {"status": "PASS"}
    elif not dobs:
        results["rule_2_dob_match"] = {"status": "PASS", "reason": "No DOB present"}
    else:
        results["rule_2_dob_match"] = {"status": "FAIL", "reason": f"DOBs differed: {dobs}"}
        overall = "FAILED"

    # Rule 3: Address matching (component-wise)
    def addr_components(addr):
        if not isinstance(addr, dict):
            return {}
        return {k: (addr.get(k, "") or "").lower().strip() for k in ["house_number","street","city","state","pincode"]}
    addresses = [addr_components(d.get("Complete Address")) for d in docs if d.get("Complete Address")]
    if not addresses:
        results["rule_3_address_match"] = {"status": "PASS", "reason": "No addresses to compare"}
    else:
        core_keys = ["house_number","city","pincode"]  # stricter
        mismatch = False
        for key in core_keys:
            vals = set(a.get(key,"") for a in addresses)
            if len(vals - {""}) > 1:
                mismatch = True
                break
        results["rule_3_address_match"] = {"status": "FAIL"} if mismatch else {"status": "PASS"}
        if mismatch:
            overall = "FAILED"

    # Rule 4: Phone matching
    phones = [re.sub(r'\D','', d.get("Phone Number",""))[-10:] for d in docs if d.get("Phone Number")]
    if phones and len(set(phones)) == 1:
        results["rule_4_phone_match"] = {"status": "PASS"}
    elif not phones:
        results["rule_4_phone_match"] = {"status": "PASS", "reason":"No phone to compare"}
    else:
        results["rule_4_phone_match"] = {"status": "FAIL", "reason": f"Phones differ: {phones}"}
        overall = "FAILED"

    # Rule 5: Father's name matching
    fathers = [d.get("Father's Name","").lower().strip() for d in docs if d.get("Father's Name")]
    if fathers and len(set([re.sub(r'\s+','',f) for f in fathers])) <= 1:
        results["rule_5_father_name_match"] = {"status":"PASS"}
    else:
        results["rule_5_father_name_match"] = {"status":"PASS" if not fathers else "FAIL"}
        if results["rule_5_father_name_match"]["status"] == "FAIL":
            overall = "FAILED"

    # Rule 6: PAN format
    pan_vals = [d.get("PAN Number","").strip().upper() for d in docs if d.get("PAN Number")]
    pan_regex = re.compile(r'^[A-Z]{5}[0-9]{4}[A-Z]$')
    if not pan_vals:
        results["rule_6_pan_format"] = {"status":"PASS", "reason":"No PAN present"}
    else:
        pan_ok = all(bool(pan_regex.match(p)) for p in pan_vals)
        results["rule_6_pan_format"] = {"status":"PASS" if pan_ok else "FAIL", "values": pan_vals}
        if not pan_ok:
            overall = "FAILED"

    # Rule 7: Aadhaar format
    aadhaars = [re.sub(r'\D','', d.get("Aadhaar Number","")) for d in docs if d.get("Aadhaar Number")]
    if not aadhaars:
        results["rule_7_aadhaar_format"] = {"status":"PASS", "reason":"No Aadhaar present"}
    else:
        aad_ok = all(len(a)==12 and a.isdigit() for a in aadhaars)
        results["rule_7_aadhaar_format"] = {"status":"PASS" if aad_ok else "FAIL", "values": aadhaars}
        if not aad_ok:
            overall = "FAILED"

    return results, overall
