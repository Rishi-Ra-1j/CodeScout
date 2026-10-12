import os
import httpx
from dotenv import load_dotenv

load_dotenv()

api_key=os.getenv("GEMINI_API_KEY")

url="https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
headers={"x-goog-api-key":api_key}
body={"contents":[{"parts":[{"text": "Explain what an API is in one sentence"}]}]}
r=httpx.post(url,headers=headers, json=body, timeout=30)
print("status",r.status_code)
print(r.json())