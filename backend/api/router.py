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
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    text_content = ""
    file_extension = file.filename.split('.')[-1].lower()
    
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
        
    # Local Offline Extraction
    structured_data = extract_entities_and_events(text_content)
    
    # DB Insertion
    case = db.query(models.Case).first()
    if not case:
        case = models.Case(title="Operation Hackathon")
        db.add(case)
        db.commit()
        db.refresh(case)
        
    doc = models.Document(case_id=case.case_id, filename=file.filename, type=file_extension.upper())
    db.add(doc)
    
    for person in structured_data.get("people", []):
        db.add(models.Person(case_id=case.case_id, name=person.get("name", "Unknown"), role=person.get("role", "Unknown")))
        
    for org in structured_data.get("organizations", []):
        db.add(models.Organization(case_id=case.case_id, name=org.get("name", "Unknown")))
        
    for veh in structured_data.get("vehicles", []):
        db.add(models.Vehicle(case_id=case.case_id, registration=veh.get("registration", "Unknown"), model=veh.get("model", "Unknown")))
        
    for ev in structured_data.get("evidence", []):
        db.add(models.Evidence(case_id=case.case_id, type=ev.get("type", "Item"), description=ev.get("description", ""), source_document=file.filename))

    for event in structured_data.get("events", []):
        db.add(models.Event(case_id=case.case_id, event=event.get("description", "Event"), location=event.get("location", ""), time=event.get("time", "")))
        
    for rel in structured_data.get("relationships", []):
        db.add(models.Relationship(case_id=case.case_id, entity1=rel.get("entity1", ""), relation=rel.get("relation", ""), entity2=rel.get("entity2", "")))

    db.commit()
    
    return {"status": "success", "structured_intelligence": structured_data}

@router.get("/cases")
def get_cases(db: Session = Depends(get_db)):
    return db.query(models.Case).all()

@router.get("/timeline/{case_id}")
def get_timeline(case_id: int, db: Session = Depends(get_db)):
    # Very basic sort by time string
    events = db.query(models.Event).filter(models.Event.case_id == case_id).all()
    return sorted(events, key=lambda x: str(x.time))

@router.get("/entities/{case_id}")
def get_entities(case_id: int, db: Session = Depends(get_db)):
    return {
        "people": db.query(models.Person).filter(models.Person.case_id == case_id).all(),
        "organizations": db.query(models.Organization).filter(models.Organization.case_id == case_id).all(),
        "vehicles": db.query(models.Vehicle).filter(models.Vehicle.case_id == case_id).all(),
        "evidence": db.query(models.Evidence).filter(models.Evidence.case_id == case_id).all(),
        "relationships": db.query(models.Relationship).filter(models.Relationship.case_id == case_id).all(),
    }

@router.get("/search")
def search_evidence(query: str, db: Session = Depends(get_db)):
    """Global search across all cases and entities."""
    return {
        "people": db.query(models.Person).filter(models.Person.name.contains(query)).all(),
        "events": db.query(models.Event).filter(models.Event.description.contains(query)).all(),
        "vehicles": db.query(models.Vehicle).filter(models.Vehicle.registration.contains(query)).all()
    }
