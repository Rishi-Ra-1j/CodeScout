from pydantic import BaseModel

class CodeSummary(BaseModel):
    summary: str
    language: str 
    functions: list[str] 
