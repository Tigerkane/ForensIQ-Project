import os
import sys
import time
import json
import re
import requests
import threading

OLLAMA_API_URL = "http://localhost:11434/api/generate"

# A global flag to stop the timer thread
stop_timer = False

def timer_thread():
    start_time = time.time()
    while not stop_timer:
        elapsed = time.time() - start_time
        # Use carriage return \r to overwrite the line with the current elapsed time
        sys.stdout.write(f"\r{Colors.WARNING}[+] Generating forensic intelligence... Elapsed: {elapsed:.1f}s{Colors.ENDC}")
        sys.stdout.flush()
        time.sleep(0.1)

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

    # Handle PDF files
    if file_path.lower().endswith('.pdf'):
        try:
            import fitz  # PyMuPDF
            text = ""
            with fitz.open(file_path) as doc:
                for page in doc:
                    text += page.get_text()
            if not text.strip():
                print(f"\n{Colors.FAIL}[ERROR] PDF file is empty or scanned (no selectable text).{Colors.ENDC}")
                return None
        except Exception as e:
            print(f"\n{Colors.FAIL}[ERROR] Failed to parse PDF: {e}{Colors.ENDC}")
            return None
    else:
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
    - "investigation_insights": Generate 5-8 AI-generated observations (e.g. "Possible insider involvement").
    - "recommended_actions": Generate 4-6 recommended investigation actions (e.g. "Seize records").
    - "people": List all people. Provide role and dynamic confidence.
    - "organizations": List companies or groups. Provide dynamic confidence.
    - "vehicles": List vehicles with registration and model. Provide dynamic confidence.
    - "weapons": Extract any weapons, firearms, blunt objects. Provide dynamic confidence.
    - "evidence": List physical/digital evidence. Include type, description, importance ("Critical", "High", "Medium", "Low"), dynamic confidence, and reasoning. EXCLUDE WEAPONS.
    - "timeline": Extract EVERY significant event. Include timestamp, location, title, description, dynamic confidence, and reasoning.
    - "relationships": Build a COMPLETE knowledge graph of connections. Include source_entity, relationship_type, target_entity, dynamic confidence, and reasoning.
    - "contradictions": List any conflicting statements or evidence.

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
      "investigation_insights": ["string"],
      "recommended_actions": ["string"],
      "timeline": [
        {{ "timestamp": "string", "location": "string", "title": "string", "description": "string", "confidence": 0.96, "reasoning": "string" }}
      ],
      "people": [{{ "name": "string", "role": "string", "confidence": 0.84 }}],
      "organizations": [{{ "name": "string", "confidence": 0.96 }}],
      "vehicles": [{{ "registration": "string", "model": "string", "confidence": 0.98 }}],
      "weapons": [{{ "type": "string", "description": "string", "confidence": 0.95 }}],
      "evidence": [{{ "type": "string", "description": "string", "importance": "string", "confidence": 0.94, "reasoning": "string" }}],
      "relationships": [{{ "source_entity": "string", "relationship_type": "string", "target_entity": "string", "confidence": 0.88, "reasoning": "string" }}],
      "contradictions": ["string"]
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

    global stop_timer
    stop_timer = False

    print(f"\n{Colors.WARNING}[+] Sending case file to local Ollama ({model_name})...{Colors.ENDC}")
    
    # Start the live timer thread
    t = threading.Thread(target=timer_thread)
    t.daemon = True
    t.start()
    
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
        
        # Stop the timer and clear the line to print the success message
        stop_timer = True
        t.join()
        sys.stdout.write("\r" + " " * 80 + "\r")  # Clear line
        print(f"{Colors.GREEN}[✔] Inference complete in {elapsed:.2f} seconds!{Colors.ENDC}\n")
        return parsed
    except Exception as e:
        stop_timer = True
        t.join()
        sys.stdout.write("\r" + " " * 80 + "\r")  # Clear line
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
    
    # 3. Insights & Recommended Actions
    print(f"{Colors.HEADER}========================================================================{Colors.ENDC}")
    print(f"{Colors.BLUE}{Colors.BOLD}                    AI INSIGHTS & RECOMMENDED ACTIONS{Colors.ENDC}")
    print(f"{Colors.HEADER}========================================================================{Colors.ENDC}")
    print(f"{Colors.BOLD}AI Observations:{Colors.ENDC}")
    for insight in data.get("investigation_insights", []):
        print(f"  • {Colors.CYAN}{insight}{Colors.ENDC}")
    print()
    print(f"{Colors.BOLD}Recommended Next Steps:{Colors.ENDC}")
    for action in data.get("recommended_actions", []):
        print(f"  [ ] {Colors.WARNING}{action}{Colors.ENDC}")
    print()

    # 4. Entities (People, Orgs, Vehicles, Weapons)
    print(f"{Colors.HEADER}========================================================================{Colors.ENDC}")
    print(f"{Colors.BLUE}{Colors.BOLD}                            ENTITIES DETECTED{Colors.ENDC}")
    print(f"{Colors.HEADER}========================================================================{Colors.ENDC}")
    print(f"{Colors.BOLD}People:{Colors.ENDC}")
    for person in data.get("people", []):
        print(f"  • {Colors.BOLD}{person.get('name')}{Colors.ENDC} - {person.get('role')} (Conf: {person.get('confidence', 0)*100:.1f}%)")
    print()
    
    orgs = data.get("organizations", [])
    if orgs:
        print(f"{Colors.BOLD}Organizations:{Colors.ENDC}")
        for org in orgs:
            print(f"  • {org.get('name')} (Conf: {org.get('confidence', 0)*100:.1f}%)")
        print()

    vehicles = data.get("vehicles", [])
    if vehicles:
        print(f"{Colors.BOLD}Vehicles:{Colors.ENDC}")
        for vehicle in vehicles:
            print(f"  • {vehicle.get('model')} [{vehicle.get('registration')}] (Conf: {vehicle.get('confidence', 0)*100:.1f}%)")
        print()

    weapons = data.get("weapons", [])
    if weapons:
        print(f"{Colors.BOLD}Weapons & Threat Objects:{Colors.ENDC}")
        for weapon in weapons:
            print(f"  • {weapon.get('type')} - {weapon.get('description')} (Conf: {weapon.get('confidence', 0)*100:.1f}%)")
        print()

    # 5. Evidence Locker
    print(f"{Colors.HEADER}========================================================================{Colors.ENDC}")
    print(f"{Colors.BLUE}{Colors.BOLD}                           EVIDENCE LOCKER & ASSETS{Colors.ENDC}")
    print(f"{Colors.HEADER}========================================================================{Colors.ENDC}")
    for item in data.get("evidence", []):
        imp_color = Colors.FAIL if item.get('importance') == 'Critical' or item.get('importance') == 'High' else Colors.WARNING
        print(f"[{imp_color}{item.get('importance')}{Colors.ENDC}] {Colors.BOLD}{item.get('type')}{Colors.ENDC}: {item.get('description')}")
        print(f"      {Colors.CYAN}Analysis:{Colors.ENDC} {item.get('reasoning')}\n")

    # 6. Timeline of Events
    print(f"{Colors.HEADER}========================================================================{Colors.ENDC}")
    print(f"{Colors.BLUE}{Colors.BOLD}                         INVESTIGATION TIMELINE{Colors.ENDC}")
    print(f"{Colors.HEADER}========================================================================{Colors.ENDC}")
    for event in data.get("timeline", []):
        print(f"[{Colors.GREEN}{event.get('timestamp')}{Colors.ENDC}] {Colors.BOLD}{event.get('title')}{Colors.ENDC} @ {event.get('location')}")
        print(f"    Details: {event.get('description')}")
        print(f"    {Colors.CYAN}Significance:{Colors.ENDC} {event.get('reasoning')}\n")

    # 7. Relationships (Knowledge Graph)
    relationships = data.get("relationships", [])
    if relationships:
        print(f"{Colors.HEADER}========================================================================{Colors.ENDC}")
        print(f"{Colors.BLUE}{Colors.BOLD}                       KNOWLEDGE GRAPH (RELATIONS){Colors.ENDC}")
        print(f"{Colors.HEADER}========================================================================{Colors.ENDC}")
        for rel in relationships:
            print(f"  {Colors.BOLD}{rel.get('source_entity')}{Colors.ENDC} ──[{Colors.WARNING}{rel.get('relationship_type')}{Colors.ENDC}]──> {Colors.BOLD}{rel.get('target_entity')}{Colors.ENDC} (Conf: {rel.get('confidence', 0)*100:.1f}%)")
            print(f"      {Colors.CYAN}Reasoning:{Colors.ENDC} {rel.get('reasoning')}\n")

    # 8. Contradictions
    contradictions = data.get("contradictions", [])
    if contradictions:
        print(f"{Colors.HEADER}========================================================================{Colors.ENDC}")
        print(f"{Colors.FAIL}{Colors.BOLD}                      INVESTIGATION CONTRADICTIONS{Colors.ENDC}")
        print(f"{Colors.HEADER}========================================================================{Colors.ENDC}")
        for contra in contradictions:
            print(f"  ⚠️ {Colors.FAIL}{contra}{Colors.ENDC}")
        print()

def main():
    clear_screen()
    print_banner()
    
    # Simple menu to select file
    print("Available Local Mock Files:")
    mock_dir = "backend/data/mock" # Adjust if your path is different
    # Fallback to current dir if mock dir not found
    if not os.path.exists(mock_dir):
        mock_dir = "."
        
    files = [f for f in os.listdir(mock_dir) if f.lower().endswith((".txt", ".pdf"))]
    
    if not files:
        print(f"{Colors.FAIL}No .txt or .pdf files found in current directory.{Colors.ENDC}")
        file_path = input("Enter path to your case file: ")
    else:
        print(" [0] Enter a custom file path...")
        for idx, f in enumerate(files):
            print(f" [{idx + 1}] {f}")
        print()
        
        user_input = input("Select a file number to analyze (or enter a custom file path directly): ").strip()
        
        # Smart path checking (even if they forget the extension)
        if os.path.exists(user_input):
            file_path = user_input
        elif os.path.exists(user_input + ".txt"):
            file_path = user_input + ".txt"
        elif os.path.exists(user_input + ".pdf"):
            file_path = user_input + ".pdf"
        else:
            try:
                choice = int(user_input) - 1
                if choice == -1:
                    custom_path = input("Enter path to your case file (.txt or .pdf): ").strip()
                    if os.path.exists(custom_path):
                        file_path = custom_path
                    elif os.path.exists(custom_path + ".txt"):
                        file_path = custom_path + ".txt"
                    elif os.path.exists(custom_path + ".pdf"):
                        file_path = custom_path + ".pdf"
                    else:
                        print(f"File not found: {custom_path}")
                        return
                elif choice < -1 or choice >= len(files):
                    print("Invalid selection.")
                    return
                else:
                    file_path = os.path.join(mock_dir, files[choice])
            except ValueError:
                print("Invalid input. Please enter a valid menu number or file path.")
                return

    # Choose model dynamically by querying local Ollama
    print("\nDetecting downloaded local models...")
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=3)
        if r.status_code == 200:
            models_data = r.json().get("models", [])
            downloaded_models = [m["name"] for m in models_data]
        else:
            downloaded_models = []
    except Exception:
        downloaded_models = []

    if downloaded_models:
        print("Select Local Model:")
        for idx, m in enumerate(downloaded_models):
            print(f" [{idx + 1}] {m}")
        print(" [0] Enter a custom model name manually...")
        print()
        
        try:
            m_choice = input("Select model (default: 1): ").strip()
            if not m_choice:
                model_name = downloaded_models[0]
            elif m_choice == "0":
                model_name = input("Enter Ollama model name: ").strip()
            else:
                m_choice = int(m_choice) - 1
                if 0 <= m_choice < len(downloaded_models):
                    model_name = downloaded_models[m_choice]
                else:
                    model_name = downloaded_models[0]
        except ValueError:
            model_name = downloaded_models[0]
    else:
        # Fallback to hardcoded list if Ollama is unreachable
        print("Select Local Model:")
        print(" [1] qwen2.5:3b")
        print(" [2] llama3.2")
        print(" [3] Enter custom name...")
        model_choice = input("Select model (default: 1): ").strip()
        if model_choice == "2":
            model_name = "llama3.2"
        elif model_choice == "3":
            model_name = input("Enter Ollama model name: ").strip()
        else:
            model_name = "qwen2.5:3b"

    result = process_file_local(file_path, model_name)
    if result:
        # Save output report locally (works for both .txt and .pdf)
        base_path = os.path.splitext(file_path)[0]
        output_file = base_path + "_forensiq_report.json"
        with open(output_file, 'w') as out:
            json.dump(result, out, indent=2)
            
        input("\nPress Enter to view the generated Forensic Report...")
        display_report(result)
        print(f"\n{Colors.GREEN}[✔] Full JSON report saved to: {output_file}{Colors.ENDC}")
        
if __name__ == "__main__":
    main()
