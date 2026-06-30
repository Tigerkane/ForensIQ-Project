import json
import re

import os
import requests

OLLAMA_API_URL = os.environ.get("OLLAMA_API_URL", "http://localhost:11434/api/generate")


def extract_entities_and_events(text: str, model_name: str = "llama3") -> dict:
    """
    Sends the cleaned text to the local Ollama LLM and enforces the strict Shared Contract JSON schema for Deep Investigation.
    """
    prompt = f"""
    You are an expert criminal intelligence AI and forensic investigator. Analyze the following text and extract deeply structured intelligence.
    Do NOT simply summarize the text. You must act as an analyst: connect evidence, calculate risks logically, identify suspicious behaviour, and explain your reasoning.
    
    CRITICAL INSTRUCTION - DYNAMIC CONFIDENCE:
    Do not default confidence scores to 0.9. Calculate realistic confidence values (e.g. 0.84, 0.99, 0.72) based on evidence strength.

    RULES:
    - "executive_summary": Write a comprehensive analytical investigation report. Answer: What happened? Why is it suspicious? What evidence supports this? What patterns are visible? What are the strongest findings?
    - "risk_analysis": Calculate a risk score (1-10), provide a dynamic confidence score (0.0-1.0), and list the exact reasons (e.g. "Weapon recovered", "Financial fraud").
    - "primary_suspect": Identify the main suspect. Include confidence, a list of reasons, and a list of supporting evidence.
    - "investigation_insights": Generate 5-8 AI-generated observations (e.g. "Possible insider involvement", "Financial fraud indicators").
    - "recommended_actions": Generate 4-6 recommended investigation actions (e.g. "Seize Blue Horizon financial records", "Recover deleted DVR footage").
    - "people": List all people. Provide role and dynamic confidence.
    - "organizations": List companies or groups. Provide dynamic confidence.
    - "vehicles": List vehicles with registration and model. Provide dynamic confidence.
    - "weapons": Extract any weapons, firearms, blunt objects, or destructive devices. Include type and description. Provide dynamic confidence.
    - "evidence": List physical/digital evidence. Include type, description, importance ("Critical", "High", "Medium", "Low"), dynamic confidence, linked people/events, and "reasoning". EXCLUDE WEAPONS FROM THIS LIST (put them in the 'weapons' array instead).
    - "timeline": Extract EVERY significant event (action, observation, transaction, communication, system change, discovery, finding). If no timestamp exists, preserve the logical order. Do not just summarize paragraphs; break the document into meaningful chronological investigation events. Include timestamp, location, title, description, entities_involved, supporting_evidence, dynamic confidence, and "reasoning" explaining its significance.
    - "relationships": Build a COMPLETE knowledge graph. Identify meaningful connections between ANY entities (Person↔Person, Person↔Device, Org↔Transaction, Event↔Evidence). Infer relationships logically from the entire text. Include source_entity, relationship_type, target_entity, dynamic confidence, supporting_evidence, and "reasoning".
    - "contradictions": List any conflicting statements or evidence.

    Return this exact JSON structure:
    {{
      "executive_summary": "string",
      "risk_analysis": {{
        "score": 8.5,
        "confidence": 0.92,
        "reasoning": ["string", "string"]
      }},
      "primary_suspect": {{
        "entity": "string",
        "confidence": 0.88,
        "reasoning": ["string", "string"],
        "supporting_evidence": ["string"]
      }},
      "investigation_insights": ["string", "string"],
      "recommended_actions": ["string", "string"],
      "timeline": [
        {{ "timestamp": "string", "location": "string", "title": "string", "description": "string", "entities_involved": "string", "supporting_evidence": "string", "confidence": 0.96, "reasoning": "string" }}
      ],
      "people": [{{ "name": "string", "role": "string", "confidence": 0.84 }}],
      "organizations": [{{ "name": "string", "confidence": 0.96 }}],
      "vehicles": [{{ "registration": "string", "model": "string", "confidence": 0.98 }}],
      "weapons": [{{ "type": "string", "description": "string", "confidence": 0.95 }}],
      "evidence": [{{ "type": "string", "description": "string", "importance": "string", "confidence": 0.94, "linked_people": "string", "linked_events": "string", "reasoning": "string" }}],
      "relationships": [{{ "source_entity": "string", "relationship_type": "string", "target_entity": "string", "confidence": 0.88, "supporting_evidence": "string", "reasoning": "string" }}],
      "contradictions": [{{ "description": "string" }}]
    }}
    
    TEXT:
    {text}
    
    Return ONLY valid JSON. No markdown, no explanation.
    """

    payload = {
        "model": model_name,
        "prompt": prompt,
        "format": "json",
        "stream": False,
        "options": {"temperature": 0.0, "num_predict": 4000, "num_ctx": 8192},
    }

    try:
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=1800)
        response.raise_for_status()
        data = response.json()

        # Robust JSON cleaning
        raw_response = data.get("response", "{}")
        raw_response = re.sub(r"```json\s*", "", raw_response)
        raw_response = re.sub(r"```\s*", "", raw_response)

        parsed_data = json.loads(raw_response)
        return parsed_data
    except Exception as e:
        print(f"LLM local extraction failed: {e}")
        return {}
