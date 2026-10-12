import json
from llm import ask_llm
from schemas import CodeSummary

code="""
def add(a,b):
    return a+b
"""

prompt=f"""Summarize this code. Return ONLY JSON with keys:
summary(string), language (string), functions (list of strings).

{code}"""

text=ask_llm(prompt,json_mode=True)["text"]
# print(repr(text))
result=CodeSummary.model_validate_json(text)
print(result.summary)
print(result.functions)
