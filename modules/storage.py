import os
import json
import logging

logger = logging.getLogger(__name__)

def save_json(data: dict, file_path: str) -> bool:
    """Save data to a JSON file with error handling."""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        logger.info(f"Successfully saved to {file_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to save JSON to {file_path}: {str(e)}")
        return False