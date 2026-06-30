import os
import sys
import time
import json
import re
import requests

OLLAMA_API_URL = "http://localhost:11434/api/generate"

# ANSI Colors for beautiful terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    print(f"{Colors.BLUE}{Colors.BOLD}")
    print(r"  ███████╗ ██████╗ ██████╗ ███████╗███╗   ██╗███████╗██╗ ██████╗ ")
    print(r"  ██╔════╝██╔═══██╗██╔══██╗██╔════╝████╗  ██║██╔════╝██║██╔═══██╗")
    print(r"  █████╗  ██║   ██║██████╔╝█████╗  ██╔██╗ ██║███████╗██║██║   ██║")
    print(r"  ██╔══╝  ██║   ██║██╔══██╗██╔══╝  ██║╚██╗██║╚════██║██║██║▄▄ ██║")
    print(r"  ██║     ╚██████╔╝██║  ██║███████╗██║ ╚████║███████║██║╚██████╔╝")
    print(r"  ╚═╝      ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝ ╚══▀▀═╝ ")
    print(f"       -- Offline Investigation Intelligence Terminal --{Colors.ENDC}\n")

def process_file_local(file_path, model_name):
    if not os.path.exists(file_path):
        print(f"\n{Colors.FAIL}[ERROR] File '{file_path}' not found.{Colors.ENDC}")
        return None

    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    prompt = f"""
    You are an expert criminal intelligence AI and forensic investigator. Analyze the following text and extract deeply structured intelligence.
    Do NOT simply summarize the text. You must act as an analyst: connect evidence, calculate risks logically, identify suspicious behaviour, and explain your reasoning.
    
    CRITICAL INSTRUCTION - DYNAMIC CONFIDENCE:
    Do not default confidence scores to 0.9. Calculate realistic confidence values (e.g. 0.84, 0.99, 0.72) based on evidence strength.

    RULES:
    - "executive_summary": Write a comprehensive analytical investigation report. Answer: What happened? Why is it suspicious? What evidence supports this? What patterns are visible? What are the strongest findings?
    - "risk_analysis": Calculate a risk score (1-10), provide a dynamic confidence score (0.0-1.0), and list the exact reasons (e.g. "Weapon recovered", "Financial fraud").
    - "primary_suspect": Identify the main suspect. Include confidence, a list of reasons, and a list of supporting evidence.
    - "timeline": Extract EVERY significant event. Include timestamp, location, title, description, dynamic confidence, and reasoning.
    - "evidence": List physical/digital evidence. Include type, description, importance ("Critical", "High", "Medium", "Low"), dynamic confidence, and reasoning.
    - "people": List key people. Provide role and confidence.

    Return this exact JSON structure:
    {{
      "executive_summary": "string",
      "risk_analysis": {{
        "score": 8.5,
        "confidence": 0.92,
        "reasoning": ["string"]
      }},
      "primary_suspect": {{
        "entity": "string",
        "confidence": 0.88,
        "reasoning": ["string"],
        "supporting_evidence": ["string"]
      }},
      "timeline": [
        {{ "timestamp": "string", "location": "string", "title": "string", "description": "string", "confidence": 0.96, "reasoning": "string" }}
      ],
      "people": [{{ "name": "string", "role": "string", "confidence": 0.84 }}],
      "evidence": [{{ "type": "string", "description": "string", "importance": "string", "confidence": 0.94, "reasoning": "string" }}]
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

    print(f"\n{Colors.WARNING}[+] Sending case file to local Ollama ({model_name})...{Colors.ENDC}")
    print(f"{Colors.WARNING}[+] Generating structured forensic intelligence. Please wait...{Colors.ENDC}")
    
    start_time = time.time()
    try:
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=1800)
        response.raise_for_status()
        data = response.json()
        raw_response = data.get("response", "{}")
        
        # Clean JSON wrappers if any
        raw_response = re.sub(r"```json\s*", "", raw_response)
        raw_response = re.sub(r"```\s*", "", raw_response)
        
        parsed = json.loads(raw_response)
        elapsed = time.time() - start_time
        print(f"{Colors.GREEN}[✔] Inference complete in {elapsed:.2f} seconds!{Colors.ENDC}\n")
        return parsed
    except Exception as e:
        print(f"\n{Colors.FAIL}[ERROR] Local extraction failed: {e}{Colors.ENDC}")
        return None

def display_report(data):
    if not data:
        return
    
    clear_screen()
    print_banner()
    
    # 1. Executive Summary
    print(f"{Colors.HEADER}========================================================================{Colors.ENDC}")
    print(f"{Colors.BLUE}{Colors.BOLD}                      EXECUTIVE FORENSIC SUMMARY{Colors.ENDC}")
    print(f"{Colors.HEADER}========================================================================{Colors.ENDC}")
    print(data.get("executive_summary", "No summary generated."))
    print()
    
    # 2. Risk & Suspect Analysis
    print(f"{Colors.HEADER}========================================================================{Colors.ENDC}")
    print(f"{Colors.BLUE}{Colors.BOLD}                      RISK & SUSPECT ASSESSMENT{Colors.ENDC}")
    print(f"{Colors.HEADER}========================================================================{Colors.ENDC}")
    
    risk = data.get("risk_analysis", {})
    suspect = data.get("primary_suspect", {})
    
    print(f"{Colors.BOLD}RISK LEVEL:{Colors.ENDC} {Colors.FAIL}{risk.get('score', 0)}/10{Colors.ENDC} (Confidence: {risk.get('confidence', 0)*100:.1f}%)")
    print(f"{Colors.BOLD}Risk Factors:{Colors.ENDC}")
    for reason in risk.get("reasoning", []):
        print(f"  - {reason}")
    print()
    
    print(f"{Colors.BOLD}PRIMARY SUSPECT:{Colors.ENDC} {Colors.WARNING}{suspect.get('entity', 'Unknown')}{Colors.ENDC} (Confidence: {suspect.get('confidence', 0)*100:.1f}%)")
    print(f"{Colors.BOLD}Involvement Reasoning:{Colors.ENDC}")
    for reason in suspect.get("reasoning", []):
        print(f"  - {reason}")
    print()
    
    # 3. People Involved
    print(f"{Colors.HEADER}========================================================================{Colors.ENDC}")
    print(f"{Colors.BLUE}{Colors.BOLD}                           PEOPLE INVOLVED{Colors.ENDC}")
    print(f"{Colors.HEADER}========================================================================{Colors.ENDC}")
    for person in data.get("people", []):
        print(f"• {Colors.BOLD}{person.get('name')}{Colors.ENDC} - Role: {person.get('role')} (Conf: {person.get('confidence', 0)*100:.1f}%)")
    print()

    # 4. Evidence Locker
    print(f"{Colors.HEADER}========================================================================{Colors.ENDC}")
    print(f"{Colors.BLUE}{Colors.BOLD}                           EVIDENCE LOCKER & ASSETS{Colors.ENDC}")
    print(f"{Colors.HEADER}========================================================================{Colors.ENDC}")
    for item in data.get("evidence", []):
        imp_color = Colors.FAIL if item.get('importance') == 'Critical' or item.get('importance') == 'High' else Colors.WARNING
        print(f"[{imp_color}{item.get('importance')}{Colors.ENDC}] {Colors.BOLD}{item.get('type')}{Colors.ENDC}: {item.get('description')}")
        print(f"      {Colors.CYAN}Analysis:{Colors.ENDC} {item.get('reasoning')}\n")

    # 5. Timeline of Events
    print(f"{Colors.HEADER}========================================================================{Colors.ENDC}")
    print(f"{Colors.BLUE}{Colors.BOLD}                         INVESTIGATION TIMELINE{Colors.ENDC}")
    print(f"{Colors.HEADER}========================================================================{Colors.ENDC}")
    for event in data.get("timeline", []):
        print(f"[{Colors.GREEN}{event.get('timestamp')}{Colors.ENDC}] {Colors.BOLD}{event.get('title')}{Colors.ENDC} @ {event.get('location')}")
        print(f"    Details: {event.get('description')}")
        print(f"    {Colors.CYAN}Significance:{Colors.ENDC} {event.get('reasoning')}\n")

def main():
    clear_screen()
    print_banner()
    
    # Simple menu to select file
    print("Available Local Mock Files:")
    mock_dir = "backend/data/mock" # Adjust if your path is different
    # Fallback to current dir if mock dir not found
    if not os.path.exists(mock_dir):
        mock_dir = "."
        
    files = [f for f in os.listdir(mock_dir) if f.endswith(".txt")]
    
    if not files:
        print(f"{Colors.FAIL}No .txt files found in current directory.{Colors.ENDC}")
        file_path = input("Enter path to your case file (.txt): ")
    else:
        for idx, f in enumerate(files):
            print(f" [{idx + 1}] {f}")
        print()
        
        try:
            choice = int(input("Select a file number to analyze: ")) - 1
            if choice < 0 or choice >= len(files):
                print("Invalid selection.")
                return
            file_path = os.path.join(mock_dir, files[choice])
        except ValueError:
            print("Invalid input.")
            return

    # Choose model
    print("\nSelect Local Model:")
    print(" [1] qwen2.5:3b")
    print(" [2] llama3.2")
    model_choice = input("Select model (default: qwen2.5:3b): ")
    model_name = "llama3.2" if model_choice == "2" else "qwen2.5:3b"

    result = process_file_local(file_path, model_name)
    if result:
        # Save output report locally
        output_file = file_path.replace(".txt", "_forensiq_report.json")
        with open(output_file, 'w') as out:
            json.dump(result, out, indent=2)
            
        input("\nPress Enter to view the generated Forensic Report...")
        display_report(result)
        print(f"\n{Colors.GREEN}[✔] Full JSON report saved to: {output_file}{Colors.ENDC}")
        
if __name__ == "__main__":
    main()
