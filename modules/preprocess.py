import re

def preprocess_text(text: str) -> str:
    if not text:
        return ""
    # Only replace O->0 when within digit contexts (e.g., "20O5" -> "2005")
    text = re.sub(r'(?<=\d)O(?=\d)', '0', text)       # O between digits -> 0
    text = re.sub(r'(?<=\d)l(?=\d)', '1', text)       # l between digits -> 1
    text = re.sub(r'(?<=\d)S(?=\d)', '5', text)       # S between digits -> 5
    # Also handle cases like "I234" -> "1234" if needed:
    text = re.sub(r'(?<=\D)l(?=\d)', '1', text)
    # Normalize spacing and remove odd symbols
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s,.-/@]', '', text)
    return text.strip()