from pydantic import ValidationError
from llm import ask_llm
from schemas import CodeSummary
def summarize_code(code: str, max_attempts: int = 3) -> CodeSummary:
    prompt = f"""Summarize this code. Return ONLY JSON with keys:
summary (string), language (string), functions (list of strings).

{code}"""
    last_error = None
    for attempt in range(max_attempts):
        text = ask_llm(prompt, json_mode=True)["text"]
        try:
            return CodeSummary.model_validate_json(text)
        except ValidationError as e:
            last_error = e
            print(f"validation failed (attempt {attempt + 1}): {e.error_count()} error(s)")
    raise ValueError(f"invalid model output after {max_attempts} attempts") from last_error

if __name__ == "__main__":
    print(summarize_code("def add(a, b):\n    return a + b"))