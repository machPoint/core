"""
Database-integrated Requirements Service
Handles PDF upload, processing, and persistent storage of extracted requirements
"""

import os
import shutil
from typing import List, Optional, Dict, Any
from pathlib import Path
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
import uuid

# Import database models from main app
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from app.database import RequirementDocumentDB, RequirementDB, AsyncSessionLocal, init_db
from app.models import ArtifactRef

# Import our PDF extractor
from pdf_extractor import PDFRequirementsExtractor, ExtractedRequirement
from real_data_generator import RealDataGenerator


class DatabaseRequirementsService:
    """Service for managing requirements documents and extracted requirements with database persistence"""
    
    def __init__(self):
        self.extractor = PDFRequirementsExtractor()
        self.upload_dir = Path(__file__).parent / "uploads"
        self.upload_dir.mkdir(exist_ok=True)
    
    async def upload_document(
        self,
        file_content: bytes,
        filename: str,
        original_filename: str,
        uploaded_by: str = "system",
        document_type: Optional[str] = None,
        mission: Optional[str] = None
    ) -> str:
        """
        Upload and store a requirements document
        Returns the document ID
        """
        async with AsyncSessionLocal() as session:
            # Generate unique filename
            file_id = str(uuid.uuid4())
            safe_filename = f"{file_id}_{filename}"
            file_path = self.upload_dir / safe_filename
            
            # Save file to disk
            with open(file_path, 'wb') as f:
                f.write(file_content)
            
            # Auto-detect document type and mission from filename
            if not document_type:
                document_type = self._detect_document_type(original_filename)
            if not mission:
                mission = self._detect_mission(original_filename)
            
            # Create database record
            doc = RequirementDocumentDB(
                id=file_id,
                filename=safe_filename,
                original_filename=original_filename,
                file_path=str(file_path),
                file_size=len(file_content),
                document_type=document_type,
                mission=mission,
                uploaded_by=uploaded_by,
                processing_status="pending",
                extraction_status="not_started"
            )
            
            session.add(doc)
            await session.commit()
            
            return file_id
    
    async def process_document(self, document_id: str) -> Dict[str, Any]:
        """
        Extract requirements from an uploaded document
        Returns processing results
        """
        async with AsyncSessionLocal() as session:
            # Get document record
            result = await session.execute(
                select(RequirementDocumentDB).where(RequirementDocumentDB.id == document_id)
            )
            doc = result.scalar_one_or_none()
            
            if not doc:
                raise ValueError(f"Document {document_id} not found")
            
            if doc.extraction_status == "completed":
                return {
                    "status": "already_completed",
                    "requirements_count": doc.requirements_extracted
                }
            
            # Update status to processing
            await session.execute(
                update(RequirementDocumentDB)
                .where(RequirementDocumentDB.id == document_id)
                .values(
                    processing_status="processing",
                    extraction_status="in_progress"
                )
            )
            await session.commit()
            
            try:
                # Extract requirements from PDF
                requirements = self.extractor.extract_from_pdf(doc.file_path)
                
                # Store extracted requirements in database
                requirement_records = []
                for req in requirements:
                    req_record = RequirementDB(
                        document_id=document_id,
                        requirement_id=req.id,
                        title=req.title,
                        text=req.text,
                        category=req.category,
                        priority=req.priority,
                        verification_method=req.verification_method,
                        source_page=req.source_page,
                        parent_section=req.parent_section,
                        tags=req.tags,
                        req_metadata={
                            "source_document": req.source_document,
                            "extraction_confidence": 0.9  # Default confidence
                        }
                    )
                    requirement_records.append(req_record)
                    session.add(req_record)
                
                # Update document status
                await session.execute(
                    update(RequirementDocumentDB)
                    .where(RequirementDocumentDB.id == document_id)
                    .values(
                        processing_status="completed",
                        extraction_status="completed",
                        requirements_extracted=len(requirements),
                        processed_at=datetime.utcnow()
                    )
                )
                
                await session.commit()
                
                return {
                    "status": "completed",
                    "requirements_count": len(requirements),
                    "document_type": doc.document_type,
                    "mission": doc.mission
                }
                
            except Exception as e:
                # Update status to failed
                await session.execute(
                    update(RequirementDocumentDB)
                    .where(RequirementDocumentDB.id == document_id)
                    .values(
                        processing_status="failed",
                        extraction_status="failed",
                        doc_metadata={"error": str(e)}
                    )
                )
                await session.commit()
                
                return {
                    "status": "failed",
                    "error": str(e)
                }
    
    async def get_documents(self, include_requirements: bool = False) -> List[Dict[str, Any]]:
        """Get all uploaded documents with optional requirements"""
        async with AsyncSessionLocal() as session:
            query = select(RequirementDocumentDB)
            if include_requirements:
                query = query.options(selectinload(RequirementDocumentDB.requirements))
            
            result = await session.execute(query)
            docs = result.scalars().all()
            
            return [self._doc_to_dict(doc, include_requirements) for doc in docs]
    
    async def get_document(self, document_id: str, include_requirements: bool = False) -> Optional[Dict[str, Any]]:
        """Get a specific document with optional requirements"""
        async with AsyncSessionLocal() as session:
            query = select(RequirementDocumentDB).where(RequirementDocumentDB.id == document_id)
            if include_requirements:
                query = query.options(selectinload(RequirementDocumentDB.requirements))
            
            result = await session.execute(query)
            doc = result.scalar_one_or_none()
            
            if doc:
                return self._doc_to_dict(doc, include_requirements)
            return None
    
    async def get_requirements(
        self,
        document_id: Optional[str] = None,
        category: Optional[str] = None,
        priority: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get requirements with optional filtering"""
        async with AsyncSessionLocal() as session:
            query = select(RequirementDB)
            
            if document_id:
                query = query.where(RequirementDB.document_id == document_id)
            if category:
                query = query.where(RequirementDB.category == category)
            if priority:
                query = query.where(RequirementDB.priority == priority)
            
            query = query.limit(limit)
            
            result = await session.execute(query)
            requirements = result.scalars().all()
            
            return [self._req_to_dict(req) for req in requirements]
    
    async def generate_artifacts_from_requirements(
        self,
        document_id: Optional[str] = None,
        force_regenerate: bool = False
    ) -> Dict[str, Any]:
        """
        Generate realistic artifacts (Jama items, Jira issues, etc.) from stored requirements
        """
        async with AsyncSessionLocal() as session:
            # Get requirements to process
            query = select(RequirementDB)
            if document_id:
                query = query.where(RequirementDB.document_id == document_id)
            
            result = await session.execute(query)
            db_requirements = result.scalars().all()
            
            if not db_requirements:
                return {"status": "no_requirements", "generated": {}}
            
            # Convert database requirements to ExtractedRequirement objects
            extracted_reqs = []
            for db_req in db_requirements:
                extracted_req = ExtractedRequirement(
                    id=db_req.requirement_id,
                    title=db_req.title,
                    text=db_req.text,
                    category=db_req.category or "general",
                    priority=db_req.priority,
                    verification_method=db_req.verification_method or "test",
                    source_page=db_req.source_page or 1,
                    source_document=f"document_{db_req.document_id}",
                    parent_section=db_req.parent_section or "",
                    tags=db_req.tags or []
                )
                extracted_reqs.append(extracted_req)
            
            # Create data generator with the extracted requirements
            generator = RealDataGenerator()
            generator.real_requirements = extracted_reqs
            generator.generate_all_data()
            
            # Track generated artifacts in database
            generated_stats = {
                "jama_items": len(generator.jama_items),
                "jira_issues": len(generator.jira_issues),
                "windchill_parts": len(generator.windchill_parts),
                "windchill_ecn": len(generator.windchill_ecn),
                "email_messages": len(generator.email_messages),
                "outlook_messages": len(generator.outlook_messages),
                "pulse_items": len(generator.pulse_items)
            }
            
            # Update requirements with generated artifact references
            for req in db_requirements:
                # Find related generated items
                jama_items = [item.global_id for item in generator.jama_items if item.fields.get("related_requirement") == req.requirement_id]
                jira_issues = [issue.key for issue in generator.jira_issues if req.requirement_id in issue.labels]
                
                await session.execute(
                    update(RequirementDB)
                    .where(RequirementDB.id == req.id)
                    .values(
                        jama_items_generated=jama_items,
                        jira_issues_generated=jira_issues,
                        updated_at=datetime.utcnow()
                    )
                )
            
            await session.commit()
            
            return {
                "status": "completed",
                "requirements_processed": len(db_requirements),
                "generated": generated_stats,
                "generator": generator  # Return generator for FDS to use
            }
    
    async def delete_document(self, document_id: str) -> bool:
        """Delete a document and all associated requirements"""
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(RequirementDocumentDB).where(RequirementDocumentDB.id == document_id)
            )
            doc = result.scalar_one_or_none()
            
            if not doc:
                return False
            
            # Delete the physical file
            try:
                os.remove(doc.file_path)
            except (OSError, FileNotFoundError):
                pass  # File might already be deleted
            
            # Delete from database (cascade will handle requirements)
            await session.delete(doc)
            await session.commit()
            
            return True
    
    def _detect_document_type(self, filename: str) -> str:
        """Auto-detect document type from filename"""
        filename_lower = filename.lower()
        
        if 'mrd' in filename_lower:
            return 'MRD'
        elif 'srd' in filename_lower:
            return 'SRD'
        elif 'icd' in filename_lower:
            return 'ICD'
        elif 'requirement' in filename_lower:
            return 'Requirements'
        elif 'specification' in filename_lower:
            return 'Specification'
        else:
            return 'Document'
    
    def _detect_mission(self, filename: str) -> str:
        """Auto-detect mission from filename"""
        filename_lower = filename.lower()
        
        if 'goes-r' in filename_lower or 'goes' in filename_lower:
            return 'GOES-R'
        elif 'jwst' in filename_lower:
            return 'JWST'
        elif 'artemis' in filename_lower:
            return 'Artemis'
        elif 'orion' in filename_lower:
            return 'Orion'
        else:
            return 'Unknown'
    
    def _doc_to_dict(self, doc: RequirementDocumentDB, include_requirements: bool = False) -> Dict[str, Any]:
        """Convert database document to dictionary"""
        result = {
            "id": doc.id,
            "filename": doc.filename,
            "original_filename": doc.original_filename,
            "file_size": doc.file_size,
            "document_type": doc.document_type,
            "mission": doc.mission,
            "version": doc.version,
            "classification": doc.classification,
            "processing_status": doc.processing_status,
            "extraction_status": doc.extraction_status,
            "requirements_extracted": doc.requirements_extracted,
            "uploaded_at": doc.uploaded_at.isoformat() if doc.uploaded_at else None,
            "processed_at": doc.processed_at.isoformat() if doc.processed_at else None,
            "uploaded_by": doc.uploaded_by,
            "metadata": doc.doc_metadata
        }
        
        if include_requirements and doc.requirements:
            result["requirements"] = [self._req_to_dict(req) for req in doc.requirements]
        
        return result
    
    def _req_to_dict(self, req: RequirementDB) -> Dict[str, Any]:
        """Convert database requirement to dictionary"""
        return {
            "id": req.id,
            "document_id": req.document_id,
            "requirement_id": req.requirement_id,
            "title": req.title,
            "text": req.text,
            "category": req.category,
            "priority": req.priority,
            "verification_method": req.verification_method,
            "source_page": req.source_page,
            "parent_section": req.parent_section,
            "tags": req.tags,
            "metadata": req.req_metadata,
            "extraction_confidence": req.extraction_confidence,
            "status": req.status,
            "extracted_at": req.extracted_at.isoformat() if req.extracted_at else None,
            "jama_items_generated": req.jama_items_generated,
            "jira_issues_generated": req.jira_issues_generated,
            "related_artifacts": req.related_artifacts
        }


# Global service instance
requirements_service = DatabaseRequirementsService()


async def initialize_requirements_db():
    """Initialize the requirements database"""
    await init_db()
    print("Requirements database initialized")