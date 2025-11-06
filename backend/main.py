"""
CORE-SE Demo Backend
FastAPI application serving as the API gateway for the React frontend.
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from app.config import get_settings
from app.routers import pulse, impact, tasks, notes, knowledge, windows, ai, config as config_router, auth, settings
from app.database import init_db

# Load environment variables
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup"""
    # await init_db()  # Disabled for now
    yield

# Initialize FastAPI app
app = FastAPI(
    title="CORE-SE Demo API",
    description="Backend API for CORE-SE engineering workspace demo",
    version="1.0.0",
    lifespan=lifespan
)

# Import auth dependencies
from app.dependencies import get_optional_user

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "core-se-api"}

# Include routers
app.include_router(auth.router, prefix="/api")  # Auth routes don't need auth
app.include_router(pulse.router, prefix="/api", dependencies=[Depends(get_optional_user)])
app.include_router(impact.router, prefix="/api", dependencies=[Depends(get_optional_user)])
app.include_router(tasks.router, prefix="/api", dependencies=[Depends(get_optional_user)])
app.include_router(notes.router, prefix="/api", dependencies=[Depends(get_optional_user)])
app.include_router(knowledge.router, prefix="/api", dependencies=[Depends(get_optional_user)])
app.include_router(windows.router, prefix="/api", dependencies=[Depends(get_optional_user)])
app.include_router(ai.router, prefix="/api", dependencies=[Depends(get_optional_user)])
app.include_router(settings.router, prefix="/api", dependencies=[Depends(get_optional_user)])
app.include_router(config_router.router, prefix="/api")  # Config doesn't need auth

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
