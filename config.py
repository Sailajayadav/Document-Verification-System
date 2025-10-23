import os

# Gemini API Configuration
API_KEY = os.getenv("GEMINI_API_KEY", "")  # Default for testing
import google.generativeai as genai
genai.configure(api_key=API_KEY)