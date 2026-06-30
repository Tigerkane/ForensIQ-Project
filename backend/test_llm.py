import sys

sys.path.append("D:\\ForensIQ project\\backend")
from services.llm import extract_entities_and_events

print("Starting extraction with qwen2.5:3b...")
result = extract_entities_and_events(
    "This is a test case about Vikas Malhotra kidnapping Aarav.", "qwen2.5:3b"
)
print("Result:", result)
