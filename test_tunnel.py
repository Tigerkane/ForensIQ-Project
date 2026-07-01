import json

import requests

url = "https://honolulu-conversion-voice-oscar.trycloudflare.com/api/generate"
payload = {
    "model": "qwen2.5:3b",
    "prompt": "Say hello in one sentence.",
    "stream": False,
    "format": "json",
    "options": {"temperature": 0.0, "num_predict": 50},
}

print("Sending request to Ollama via Cloudflare tunnel...")
try:
    r = requests.post(url, json=payload, timeout=120)
    print(f"Status: {r.status_code}")
    print(f"Response: {r.text[:500]}")
except Exception as e:
    print(f"Error: {e}")
