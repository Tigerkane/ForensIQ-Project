import json
import requests

OLLAMA_API_URL = "http://localhost:11434/api/generate"
# Assuming the user is running Ollama locally with qwen2.5:3b or phi3

def extract_entities_and_events(text: str) -> dict:
    """
    Sends the cleaned text to the local Ollama LLM and enforces JSON output.
    """
    prompt = f"""
    You are an expert criminal intelligence AI. Extract the following from the provided text:
    - people: list of objects with 'name' and 'role' (e.g., Suspect, Witness, Officer)
    - locations: list of addresses or places
    - events: list of chronological events with 'time', 'location', and 'description'
    - evidence: list of items found
    
    TEXT:
    {text}
    
    Return ONLY a valid JSON object matching this schema. Do not include markdown formatting or conversational text.
    """
    
    payload = {
        "model": "qwen2.5:3b", # Fallback to tinyllama if qwen isn't pulled
        "prompt": prompt,
        "format": "json", # Ollama's native structured JSON output constraint
        "stream": False,
        "options": {
            "temperature": 0.0 # Zero temperature for deterministic extraction
        }
    }
    
    try:
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        return json.loads(data.get("response", "{}"))
    except Exception as e:
        print(f"LLM local extraction failed: {e}")
        return {"people": [], "locations": [], "events": [], "evidence": []}
