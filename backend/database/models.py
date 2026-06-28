from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Case(Base):
    __tablename__ = "cases"
    case_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="Open")
    
    events = relationship("Event", back_populates="case")
    people = relationship("Person", back_populates="case")

class Event(Base):
    __tablename__ = "events"
    event_id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.case_id"))
    event = Column(String)
    time = Column(DateTime, nullable=True)
    location = Column(String, nullable=True)
    description = Column(Text)
    
    case = relationship("Case", back_populates="events")

class Person(Base):
    __tablename__ = "people"
    person_id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.case_id"))
    name = Column(String, index=True)
    role = Column(String) # Suspect, Witness, Officer, Victim
    
    case = relationship("Case", back_populates="people")

class Document(Base):
    __tablename__ = "documents"
    document_id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.case_id"))
    filename = Column(String)
    type = Column(String) # PDF, Image, Audio
    processed_at = Column(DateTime, default=datetime.utcnow)
