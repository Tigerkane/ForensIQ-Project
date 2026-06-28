import json
import requests

OLLAMA_API_URL = "http://localhost:11434/api/generate"

def extract_entities_and_events(text: str) -> dict:
    """
    Sends the cleaned text to the local Ollama LLM and enforces massive structured JSON output.
    """
    prompt = f"""
    You are an expert criminal intelligence AI. Extract the following from the provided text:
    - document_type: string (e.g., FIR, Witness Statement)
    - people: list of objects with 'name' and 'role'
    - locations: list of objects with 'name'
    - organizations: list of objects with 'name'
    - vehicles: list of objects with 'registration' and 'model'
    - weapons: list of objects with 'type'
    - events: list of chronological events with 'time', 'location', and 'description'
    - financial_transactions: list of objects with 'description'
    - evidence: list of objects with 'type' and 'description'
    - relationships: list of objects with 'entity1', 'relation', 'entity2'
    - contradictions: list of objects with 'description' (e.g., conflicting timestamps)
    - root_cause: object with 'entity_name' and 'reasoning' explaining who or what is the primary suspect or main cause of the incident
    
    TEXT:
    {text}
    
    Return ONLY a valid JSON object matching this schema. Do not include markdown formatting or conversational text.
    """
    
    payload = {
        "model": "qwen2.5:3b",
        "prompt": prompt,
        "format": "json", 
        "stream": False,
        "options": {
            "temperature": 0.0,
            "num_predict": 2048 # Ensure it doesn't cut off long JSONs
        }
    }
    
    try:
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        return json.loads(data.get("response", "{}"))
    except Exception as e:
        print(f"LLM local extraction failed: {e}")
        return {}
