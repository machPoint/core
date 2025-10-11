"""
Fake Data Service (FDS) for CORE-SE Demo
Provides mock data for Jama, Jira, Windchill, Email, Outlook systems
"""

from fastapi import FastAPI, Query, Header, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from typing import Optional, List
import asyncio
from datetime import datetime, timedelta
import random
import base64
from pydantic import BaseModel

from data_generator import DataGenerator
from database_requirements_service import requirements_service, initialize_requirements_db
from models import *

# Document upload model
class DocumentUpload(BaseModel):
    filename: str
    original_filename: str
    file_content: str  # base64 encoded
    uploaded_by: str = "system"
    document_type: Optional[str] = None
    mission: Optional[str] = None

app = FastAPI(
    title="CORE-SE Fake Data Service",
    description="Mock data service for engineering systems",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize data generator
data_gen = DataGenerator()

# Global generator that can be replaced with database-generated data
current_generator = data_gen

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    await initialize_requirements_db()

# Mock latency simulation
async def simulate_latency(latency_header: Optional[str] = None):
    """Simulate network latency if specified"""
    if latency_header:
        try:
            delay = float(latency_header)
            await asyncio.sleep(min(delay, 5.0))  # Cap at 5 seconds
        except ValueError:
            pass

# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "core-se-fds"}

# Admin endpoints
@app.post("/mock/admin/seed")
async def seed_data():
    """Reset and regenerate all mock data"""
    global current_generator
    
    # Try to generate from database requirements first
    try:
        result = await requirements_service.generate_artifacts_from_requirements()
        if result["status"] == "completed":
            current_generator = result["generator"]
            return {
                "status": "success", 
                "message": f"Mock data regenerated from {result['requirements_processed']} requirements",
                "source": "database_requirements",
                "generated": result["generated"]
            }
    except Exception as e:
        print(f"Failed to generate from database: {e}")
    
    # Fallback to synthetic data generation
    data_gen.generate_all_data()
    current_generator = data_gen
    return {"status": "success", "message": "Mock data regenerated (synthetic)", "source": "synthetic"}

# Requirements management endpoints
@app.get("/mock/admin/documents")
async def get_documents():
    """Get all uploaded documents"""
    documents = await requirements_service.get_documents(include_requirements=False)
    return {"documents": documents}

@app.get("/mock/admin/documents/{document_id}")
async def get_document(document_id: str):
    """Get specific document with requirements"""
    document = await requirements_service.get_document(document_id, include_requirements=True)
    if not document:
        return {"error": "Document not found"}, 404
    return document

@app.post("/mock/admin/documents/{document_id}/process")
async def process_document(document_id: str):
    """Process document to extract requirements"""
    result = await requirements_service.process_document(document_id)
    return result

@app.delete("/mock/admin/documents/{document_id}")
async def delete_document(document_id: str):
    """Delete document and all requirements"""
    success = await requirements_service.delete_document(document_id)
    if success:
        return {"status": "success", "message": "Document deleted"}
    else:
        return {"error": "Document not found"}, 404

@app.get("/mock/admin/requirements")
async def get_requirements(
    document_id: Optional[str] = None,
    category: Optional[str] = None,
    priority: Optional[str] = None,
    limit: int = 100
):
    """Get requirements with filtering"""
    requirements = await requirements_service.get_requirements(
        document_id=document_id,
        category=category, 
        priority=priority,
        limit=limit
    )
    return {"requirements": requirements}

@app.post("/mock/admin/generate-from-requirements")
async def generate_from_requirements(document_id: Optional[str] = None):
    """Generate artifacts from stored requirements"""
    global current_generator
    
    result = await requirements_service.generate_artifacts_from_requirements(document_id)
    if result["status"] == "completed":
        current_generator = result["generator"]
    
    return result

@app.post("/mock/admin/upload-document")
async def upload_document(document: DocumentUpload):
    """Upload a requirements document for processing"""
    try:
        # Decode base64 content
        file_content = base64.b64decode(document.file_content)
        
        # Upload to database service
        document_id = await requirements_service.upload_document(
            file_content=file_content,
            filename=document.filename,
            original_filename=document.original_filename,
            uploaded_by=document.uploaded_by,
            document_type=document.document_type,
            mission=document.mission
        )
        
        return {
            "status": "success",
            "message": "Document uploaded successfully",
            "document_id": document_id
        }
        
    except Exception as e:
        return {
            "error": "Failed to upload document",
            "details": str(e)
        }

# Jama endpoints
@app.get("/mock/jama/items", response_model=List[JamaItem])
async def get_jama_items(
    page: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=100),
    q: Optional[str] = Query(None),
    type: Optional[str] = Query(None),
    x_mock_latency: Optional[str] = Header(None)
):
    """Get Jama requirements/items"""
    await simulate_latency(x_mock_latency)
    return current_generator.get_jama_items(page=page, size=size, query=q, item_type=type)

@app.get("/mock/jama/relationships", response_model=List[JamaRelationship])
async def get_jama_relationships(
    item_id: Optional[str] = Query(None),
    x_mock_latency: Optional[str] = Header(None)
):
    """Get Jama relationships"""
    await simulate_latency(x_mock_latency)
    return current_generator.get_jama_relationships(item_id=item_id)

# Jira endpoints
@app.get("/mock/jira/issues", response_model=List[JiraIssue])
async def get_jira_issues(
    page: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=100),
    q: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    x_mock_latency: Optional[str] = Header(None)
):
    """Get Jira issues"""
    await simulate_latency(x_mock_latency)
    return current_generator.get_jira_issues(page=page, size=size, query=q, status=status)

@app.get("/mock/jira/links", response_model=List[JiraLink])
async def get_jira_links(
    issue_id: Optional[str] = Query(None),
    x_mock_latency: Optional[str] = Header(None)
):
    """Get Jira issue links"""
    await simulate_latency(x_mock_latency)
    return current_generator.get_jira_links(issue_id=issue_id)

# Windchill endpoints
@app.get("/mock/windchill/parts", response_model=List[WindchillPart])
async def get_windchill_parts(
    page: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=100),
    q: Optional[str] = Query(None),
    x_mock_latency: Optional[str] = Header(None)
):
    """Get Windchill parts"""
    await simulate_latency(x_mock_latency)
    return current_generator.get_windchill_parts(page=page, size=size, query=q)

@app.get("/mock/windchill/bom", response_model=List[WindchillBOM])
async def get_windchill_bom(
    part_id: Optional[str] = Query(None),
    x_mock_latency: Optional[str] = Header(None)
):
    """Get Windchill Bill of Materials"""
    await simulate_latency(x_mock_latency)
    return current_generator.get_windchill_bom(part_id=part_id)

@app.get("/mock/windchill/ecn", response_model=List[WindchillECN])
async def get_windchill_ecn(
    status: Optional[str] = Query(None),
    x_mock_latency: Optional[str] = Header(None)
):
    """Get Windchill Engineering Change Notices"""
    await simulate_latency(x_mock_latency)
    return current_generator.get_windchill_ecn(status=status)

# Email and Outlook endpoints
@app.get("/mock/email/messages", response_model=List[EmailMessage])
async def get_email_messages(
    since: Optional[datetime] = Query(None),
    x_mock_latency: Optional[str] = Header(None)
):
    """Get email messages"""
    await simulate_latency(x_mock_latency)
    return current_generator.get_email_messages(since=since)

@app.get("/mock/outlook/messages", response_model=List[OutlookMessage])
async def get_outlook_messages(
    since: Optional[datetime] = Query(None),
    x_mock_latency: Optional[str] = Header(None)
):
    """Get Outlook messages"""
    await simulate_latency(x_mock_latency)
    return current_generator.get_outlook_messages(since=since)

# Aggregated endpoints
@app.get("/mock/pulse", response_model=List[MockPulseItem])
async def get_pulse(
    since: Optional[datetime] = Query(None),
    sources: Optional[str] = Query(None),
    types: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    x_mock_latency: Optional[str] = Header(None)
):
    """Get aggregated pulse feed"""
    await simulate_latency(x_mock_latency)
    
    # Parse comma-separated filters
    source_list = sources.split(",") if sources else None
    type_list = types.split(",") if types else None
    
    return current_generator.get_pulse_feed(
        since=since,
        sources=source_list,
        types=type_list,
        limit=limit
    )

@app.get("/mock/impact/{entity_id}", response_model=MockImpactResult)
async def get_impact_analysis(
    entity_id: str,
    depth: int = Query(2, ge=1, le=5),
    x_mock_latency: Optional[str] = Header(None)
):
    """Get impact analysis for an entity"""
    await simulate_latency(x_mock_latency)
    return current_generator.get_impact_analysis(entity_id=entity_id, depth=depth)

@app.get("/mock/graph/trace", response_model=TraceGraph)
async def get_trace_graph(
    root_id: Optional[str] = Query(None),
    x_mock_latency: Optional[str] = Header(None)
):
    """Get trace graph data"""
    await simulate_latency(x_mock_latency)
    return current_generator.get_trace_graph(root_id=root_id)

# HTML mock windows for read-only views
@app.get("/mock/windows/{tool}/{item_id}")
async def get_mock_window(tool: str, item_id: str):
    """Return mock HTML for read-only windows"""
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{tool.upper()} - {item_id}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
            .watermark {{ 
                position: fixed; top: 10px; right: 10px; 
                background: #ff6b6b; color: white; padding: 5px 10px; 
                border-radius: 4px; font-weight: bold; z-index: 1000;
            }}
            .content {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .header {{ border-bottom: 2px solid #007bff; padding-bottom: 10px; margin-bottom: 20px; }}
            .field {{ margin: 10px 0; }}
            .label {{ font-weight: bold; color: #555; }}
        </style>
    </head>
    <body>
        <div class="watermark">READ-ONLY DEMO</div>
        <div class="content">
            <div class="header">
                <h1>{tool.upper()} - {item_id}</h1>
                <p style="color: #666;">Mock {tool} system view</p>
            </div>
            
            {current_generator.get_mock_window_content(tool, item_id)}
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)
