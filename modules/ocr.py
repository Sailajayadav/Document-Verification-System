from PIL import Image
import google.generativeai as genai
import logging
from typing import Optional

# Configure Gemini API (moved to config.py)
logger = logging.getLogger(__name__)

def extract_text_from_image(image_path: str) -> Optional[str]:
    """
    Extract text from an image using Gemini API.
    Handles edge cases like invalid files or API errors.
    """
    try:
        img = Image.open(image_path).convert("RGB")
        model = genai.GenerativeModel("gemini-2.5-flash")
        prompt = "Extract and return the handwritten or printed text from this image. Do not include any extra text in the response."
        response = model.generate_content([prompt, img])
        text = response.text.strip()
        if not text:
            logger.warning(f"No text extracted from {image_path}")
        print(text)
        return text
    except FileNotFoundError:
        logger.error(f"Image file not found: {image_path}")
        return None
    except Exception as e:
        logger.error(f"OCR error for {image_path}: {str(e)}")
        return None