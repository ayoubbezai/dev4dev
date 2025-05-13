"""
Configuration settings for the project.
Contains API keys, model settings and other configuration parameters.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys - Make sure to add these to your .env file
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  
LAMA_API_KEY = os.getenv("LAMA_API_KEY")  


os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY   
os.environ["GEMINI_API_KEY"] = GOOGLE_API_KEY  

# Model Configuration
GEMINI_MODEL = "gemini-pro"  

# Agent Configuration
MAX_ITERATIONS = 3
TEMPERATURE = 0.5
VERBOSE = True

PDF_CHUNK_SIZE = 1000
PDF_CHUNK_OVERLAP = 200
