"""
Startup script for Fake Data Service
"""

import uvicorn
from main import app

if __name__ == "__main__":
    print("Starting CORE-SE Fake Data Service...")
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8001,
        reload=True,
        log_level="info"
    )
