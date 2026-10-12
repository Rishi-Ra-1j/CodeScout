from fastapi import FastAPI, HTTPException
import httpx
import logging
from pydantic import BaseModel
from schemas import CodeSummary
from summarizer import summarize_code

app = FastAPI()

logger = logging.getLogger("codescout")

class SummarizeRequest(BaseModel):
    code: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/summarize", response_model=CodeSummary)
def summarize(req: SummarizeRequest):
    try:
        return summarize_code(req.code)
    except ValueError as e:
        logger.error("Invalid model output: %s",e)
        raise HTTPException(status_code=502, detail="Model returned invalid output")
    except httpx.HTTPError as e:
        logger.error("LLM call failed: %s",e)
        raise HTTPException(status_code=503, detail="Model service unavailable")