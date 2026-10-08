import os
import httpx
import time
import json
from dotenv import load_dotenv

load_dotenv()

api_key=os.getenv("GEMINI_API_KEY")

URL="https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"  
RETRY_STATUS = {429, 500, 502, 503, 504}
def log_call(record: dict) -> None:
    with open("call.json1", "a") as f:
        f.write(json.dumps(record)+ "\n")

def ask_llm(prompt: str,max_retries: int=3) -> dict:
    headers = {"x-goog-api-key":api_key}
    body={
        "contents":[{"parts":[{"text":prompt}]}],
        "generationConfig": {"thinkingConfig": {"thinkingBudget": 0}},
    }
    start=time.perf_counter()
    for attempt in range(max_retries + 1) : 
        try:
            r=httpx.post(URL, headers=headers, json=body,timeout=30)
        except httpx.TimeoutException:
            if attempt == max_retries:
                raise
            print(f"timeout, retry {attempt+1}")
            time.sleep(2**attempt)
            continue
        if r.status_code in RETRY_STATUS and attempt < max_retries:
            print(f"status {r.status_code}, retry {attempt+1}")
            time.sleep(2**attempt)
            continue  
        r.raise_for_status()
        data=r.json()
        usage = data["usageMetadata"]
        latency_ms = round((time.perf_counter()-start)*1000)
        result = {
            "text": data["candidates"][0]["content"]["parts"][0]["text"],
            "prompt_tokens": usage["promptTokenCount"],
            "output_tokens": usage["candidatesTokenCount"],
            "thinking_tokens": usage.get("thoughtsTokenCount", 0),
            "latency_ms": latency_ms,
        }
        log_call({"ts":time.time(),**{k: v for k, v in result.items() if k!= "text"}})
        return result


if __name__ == "__main__" :
    result= ask_llm("Explain what an API is in one sentence.")
    print(result)
