"""
Configuration file

Loads environment variables for API keys.
NEVER hardcode keys in code.
"""

import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# API key for Vector Database (Vectorize / Hindsight)
VECTORIZE_API_KEY = os.getenv("VECTORIZE_API_KEY")
HINDSIGHT_URL = os.getenv("HINDSIGHT_URL", "http://localhost:8888")

# API key for Groq LLM
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
