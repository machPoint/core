"""
Database setup and SQLAlchemy models for CORE-SE Demo
"""

from sqlalchemy import Column, String, Text, DateTime, JSON, Integer, Boolean, Float, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from datetime import datetime
import uuid
import json

from app.config import get_settings

Base = declarative_base()

class TaskDB(Base):
    """SQLAlchemy model for tasks"""
    __tablename__ = "tasks"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(Text)
    status = Column(String, default="open")
    priority = Column(String, default="medium")
    assignee = Column(String)
    due_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    context_artifacts = Column(JSON, default=list)
    subtasks = Column(JSON, default=list)


class NoteDB(Base):
    """SQLAlchemy model for notes"""
    __tablename__ = "notes"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    citations = Column(JSON, default=list)
    tags = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    author = Column(String)


class RequirementDocumentDB(Base):
    """SQLAlchemy model for uploaded requirements documents"""
    __tablename__ = "requirement_documents"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    filename = Column(String, nullable=False)
    original_filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)  # Path to stored PDF
    file_size = Column(Integer)
    mime_type = Column(String, default="application/pdf")
    
    # Document metadata
    document_type = Column(String)  # 'MRD', 'SRD', 'ICD', etc.
    mission = Column(String)  # 'GOES-R', 'JWST', etc.
    version = Column(String)
    classification = Column(String)  # 'unclassified', 'restricted', etc.
    
    # Processing status
    processing_status = Column(String, default="pending")  # pending, processing, completed, failed
    extraction_status = Column(String, default="not_started")  # not_started, in_progress, completed, failed
    requirements_extracted = Column(Integer, default=0)
    
    # Timestamps
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # User who uploaded
    uploaded_by = Column(String)
    
    # Additional metadata
    doc_metadata = Column(JSON, default=dict)
    
    # Relationship to extracted requirements
    requirements = relationship("RequirementDB", back_populates="document", cascade="all, delete-orphan")


class RequirementDB(Base):
    """SQLAlchemy model for extracted requirements"""
    __tablename__ = "requirements"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Link to source document
    document_id = Column(String, ForeignKey("requirement_documents.id"), nullable=False)
    document = relationship("RequirementDocumentDB", back_populates="requirements")
    
    # Requirement identification
    requirement_id = Column(String, nullable=False)  # MRD-001, REQ-123, etc.
    title = Column(String, nullable=False)
    text = Column(Text, nullable=False)
    
    # Classification and metadata
    category = Column(String)  # instrument, spacecraft, ground, data, etc.
    priority = Column(String, default="medium")  # critical, high, medium, low
    verification_method = Column(String)  # test, analysis, inspection, demonstration
    
    # Source location in document
    source_page = Column(Integer)
    parent_section = Column(String)
    
    # Extracted tags and metadata
    tags = Column(JSON, default=list)
    req_metadata = Column(JSON, default=dict)
    
    # Processing confidence
    extraction_confidence = Column(Float, default=1.0)  # 0.0 - 1.0
    
    # Status
    status = Column(String, default="active")  # active, deprecated, superseded
    
    # Timestamps
    extracted_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Generated artifacts tracking
    jama_items_generated = Column(JSON, default=list)  # List of generated Jama item IDs
    jira_issues_generated = Column(JSON, default=list)  # List of generated Jira issue IDs
    related_artifacts = Column(JSON, default=list)  # List of all related artifact references


# Database setup
settings = get_settings()

if settings.DATABASE_URL.startswith("sqlite"):
    # Use aiosqlite for async SQLite
    async_database_url = settings.DATABASE_URL.replace("sqlite://", "sqlite+aiosqlite://")
    engine = create_async_engine(async_database_url, echo=False)
else:
    engine = create_async_engine(settings.DATABASE_URL, echo=False)

AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def init_db():
    """Initialize database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncSession:
    """Get database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
