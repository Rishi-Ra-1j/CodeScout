from pydantic import ValidationError
from schemas import CodeSummary

good = '{"summary": "adds numbers", "language": "python", "functions": ["add"]}'
bad = '{"summary": "x", "language": "python", "functions": "add"}'

print(CodeSummary.model_validate_json(good).functions)

try:
    CodeSummary.model_validate_json(bad)
except ValidationError as e:
    print(e)