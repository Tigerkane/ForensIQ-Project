from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Case(Base):
    __tablename__ = "cases"
    case_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    summary = Column(Text, nullable=True)
    risk_score = Column(Float, nullable=True)
    risk_confidence = Column(Float, nullable=True)
    risk_reasoning = Column(Text, nullable=True) # Stored as JSON string array
    primary_suspect_name = Column(String, nullable=True)
    primary_suspect_confidence = Column(Float, nullable=True)
    primary_suspect_reasoning = Column(Text, nullable=True) # JSON string array
    investigation_insights = Column(Text, nullable=True) # JSON string array
    recommended_actions = Column(Text, nullable=True) # JSON string array
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="Open")
    
    events = relationship("Event", back_populates="case")
    people = relationship("Person", back_populates="case")
    organizations = relationship("Organization", back_populates="case")
    vehicles = relationship("Vehicle", back_populates="case")
    evidence = relationship("Evidence", back_populates="case")
    relationships = relationship("Relationship", back_populates="case")
    documents = relationship("Document", back_populates="case")

class Event(Base):
    __tablename__ = "events"
    event_id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.case_id"))
    event = Column(String)
    time = Column(String, nullable=True) 
    location = Column(String, nullable=True)
    description = Column(Text)
    entities_involved = Column(String, nullable=True) # Comma separated entities
    supporting_evidence = Column(String, nullable=True)
    reasoning = Column(Text, nullable=True)
    confidence = Column(Float, nullable=True)
    
    case = relationship("Case", back_populates="events")

class Person(Base):
    __tablename__ = "people"
    person_id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.case_id"))
    name = Column(String, index=True)
    role = Column(String) 
    confidence = Column(Float, nullable=True)
    
    case = relationship("Case", back_populates="people")

class Organization(Base):
    __tablename__ = "organizations"
    organization_id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.case_id"))
    name = Column(String, index=True)
    confidence = Column(Float, nullable=True)
    
    case = relationship("Case", back_populates="organizations")

class Vehicle(Base):
    __tablename__ = "vehicles"
    vehicle_id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.case_id"))
    registration = Column(String, index=True)
    model = Column(String)
    confidence = Column(Float, nullable=True)
    
    case = relationship("Case", back_populates="vehicles")

class Evidence(Base):
    __tablename__ = "evidence"
    evidence_id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.case_id"))
    type = Column(String)
    description = Column(Text)
    importance = Column(String, nullable=True) # High, Medium, Low
    linked_people = Column(String, nullable=True)
    linked_events = Column(String, nullable=True)
    reasoning = Column(Text, nullable=True)
    confidence = Column(Float, nullable=True)
    source_document = Column(String)
    
    case = relationship("Case", back_populates="evidence")

class Relationship(Base):
    __tablename__ = "relationships"
    relationship_id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.case_id"))
    entity1 = Column(String, index=True)
    relation = Column(String)
    entity2 = Column(String, index=True)
    evidence_reference = Column(String, nullable=True)
    supporting_evidence = Column(Text, nullable=True)
    reasoning = Column(Text, nullable=True)
    confidence = Column(Float, nullable=True)
    
    case = relationship("Case", back_populates="relationships")

class Document(Base):
    __tablename__ = "documents"
    document_id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.case_id"))
    filename = Column(String)
    type = Column(String)
    processed_at = Column(DateTime, default=datetime.utcnow)
    
    case = relationship("Case", back_populates="documents")
