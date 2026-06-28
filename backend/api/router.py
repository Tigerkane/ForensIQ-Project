from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from database import models
from processors.pdf import extract_text_from_pdf
from processors.image import extract_text_from_image
from processors.audio import extract_text_from_audio
from services.llm import extract_entities_and_events
import os
import json
import shutil
import re

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
        
    # Local Offline Extraction (Shared Contract)
    structured_data = extract_entities_and_events(text_content)
    
    risk_analysis = structured_data.get("risk_analysis", {})
    primary_suspect = structured_data.get("primary_suspect", {})
    insights = structured_data.get("investigation_insights", [])
    recommended_actions = structured_data.get("recommended_actions", [])
    
    # DB Insertion: Create a NEW Case for every document to support Master Database View
    case = models.Case(
        title=f"Incident: {file.filename}",
        summary=structured_data.get("executive_summary", ""),
        risk_score=risk_analysis.get("score", 0.0),
        risk_confidence=risk_analysis.get("confidence", 0.0),
        risk_reasoning=json.dumps(risk_analysis.get("reasoning", [])),
        primary_suspect_name=primary_suspect.get("entity", ""),
        primary_suspect_confidence=primary_suspect.get("confidence", 0.0),
        primary_suspect_reasoning=json.dumps(primary_suspect.get("reasoning", [])),
        investigation_insights=json.dumps(insights),
        recommended_actions=json.dumps(recommended_actions)
    )
    db.add(case)
    db.commit()
    db.refresh(case)
        
    doc = models.Document(case_id=case.case_id, filename=file.filename, type=file_extension.upper())
    db.add(doc)
    
    for person in structured_data.get("people", []):
        db.add(models.Person(
            case_id=case.case_id, 
            name=person.get("name", "Unknown"), 
            role=person.get("role", "Unknown"), 
            confidence=person.get("confidence", 0.0)
        ))
        
    for org in structured_data.get("organizations", []):
        db.add(models.Organization(
            case_id=case.case_id, 
            name=org.get("name", "Unknown"),
            confidence=org.get("confidence", 0.0)
        ))
        
    for veh in structured_data.get("vehicles", []):
        db.add(models.Vehicle(case_id=case.case_id, registration=veh.get("registration", ""), model=veh.get("model", ""), confidence=veh.get("confidence", 0.0)))
        
    for wep in structured_data.get("weapons", []):
        db.add(models.Weapon(case_id=case.case_id, type=wep.get("type", ""), description=wep.get("description", ""), confidence=wep.get("confidence", 0.0)))
        
    for ev in structured_data.get("evidence", []):
        db.add(models.Evidence(
            case_id=case.case_id, 
            type=ev.get("type", "Item"), 
            description=ev.get("description", ""), 
            importance=ev.get("importance", "Medium"),
            linked_people=ev.get("linked_people", ""),
            linked_events=ev.get("linked_events", ""),
            reasoning=ev.get("reasoning", ""),
            confidence=ev.get("confidence", 0.0),
            source_document=file.filename
        ))

    for event in structured_data.get("timeline", []):
        db.add(models.Event(
            case_id=case.case_id, 
            event=event.get("title", "Event"), 
            location=event.get("location", ""), 
            time=event.get("timestamp", ""),
            description=event.get("description", ""),
            entities_involved=event.get("entities_involved", ""),
            supporting_evidence=event.get("supporting_evidence", ""),
            reasoning=event.get("reasoning", ""),
            confidence=event.get("confidence", 0.0)
        ))
        
    for rel in structured_data.get("relationships", []):
        db.add(models.Relationship(
            case_id=case.case_id, 
            entity1=rel.get("source_entity", ""), 
            relation=rel.get("relationship_type", ""), 
            entity2=rel.get("target_entity", ""),
            supporting_evidence=rel.get("supporting_evidence", ""),
            reasoning=rel.get("reasoning", ""),
            confidence=rel.get("confidence", 0.0)
        ))

    db.commit()
    
    return {"status": "success", "structured_intelligence": structured_data}


@router.get("/search")
def search_evidence(query: str, db: Session = Depends(get_db)):
    """Global search across all cases and entities."""
    return {
        "people": db.query(models.Person).filter(models.Person.name.contains(query)).all(),
        "events": db.query(models.Event).filter(models.Event.description.contains(query)).all(),
        "vehicles": db.query(models.Vehicle).filter(models.Vehicle.registration.contains(query)).all()
    }
