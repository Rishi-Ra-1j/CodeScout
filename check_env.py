import os
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("GEMINI_API_KEY")
print("key loaded: ", key is not None)
print("key length: ", len(key) if key else 0)
