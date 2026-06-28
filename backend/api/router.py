from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from database import models
from processors.pdf import extract_text_from_pdf
from processors.image import extract_text_from_image
from processors.audio import extract_text_from_audio
from services.llm import extract_entities_and_events
import os
import shutil

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/process")
async def process_evidence(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    1. Ingests file
    2. Identifies modality and extracts text locally
    3. Runs local LLM for JSON structuring
    4. Saves to SQLite
    """
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    text_content = ""
    file_extension = file.filename.split('.')[-1].lower()
    
    # Step 1 & 2: Modality Extraction
    if file_extension in ['txt']:
        with open(file_path, "r", encoding="utf-8") as f:
            text_content = f.read()
    elif file_extension in ['pdf']:
        text_content = extract_text_from_pdf(file_path)
    elif file_extension in ['png', 'jpg', 'jpeg']:
        text_content = extract_text_from_image(file_path)
    elif file_extension in ['mp3', 'wav', 'm4a']:
        text_content = extract_text_from_audio(file_path)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file format.")
        
    if not text_content:
        raise HTTPException(status_code=500, detail="Failed to extract text from evidence.")
        
    # Step 3: LLM Extraction (Offline)
    structured_data = extract_entities_and_events(text_content)
    
    # Step 4: Save to DB (Create Case if none exists for this demo)
    case = db.query(models.Case).first()
    if not case:
        case = models.Case(title="Hackathon Demo Case")
        db.add(case)
        db.commit()
        db.refresh(case)
        
    # Add Document
    doc = models.Document(case_id=case.case_id, filename=file.filename, type=file_extension.upper())
    db.add(doc)
    
    # Add People
    for person in structured_data.get("people", []):
        p = models.Person(case_id=case.case_id, name=person.get("name", "Unknown"), role=person.get("role", "Unknown"))
        db.add(p)
        
    # Add Events
    for event in structured_data.get("events", []):
        e = models.Event(case_id=case.case_id, event=event.get("description", "Unknown Event"), location=event.get("location", "Unknown"))
        db.add(e)
        
    db.commit()
    
    return {
        "status": "success", 
        "extracted_text_preview": text_content[:200] + "...", 
        "structured_intelligence": structured_data
    }
