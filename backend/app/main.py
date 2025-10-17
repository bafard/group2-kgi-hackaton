from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from app.routes import health, upload, detection, pdf_embeddings, chat, system_prompt, user_management, auth, sql_rag, database, ollama

# Create FastAPI instance with increased file size limits
app = FastAPI(
    title="FastAPI Backend Service",
    description="A FastAPI backend service with health check, file upload, PDF embeddings, and chat completion endpoints",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure maximum request size (500MB = 500 * 1024 * 1024 bytes)
app.state.max_request_size = 500 * 1024 * 1024

# Add middleware for handling large file uploads
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import json

class LargeFileMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip content-length check for file upload endpoints
        if "/upload" in str(request.url):
            # Allow very large file uploads (500MB)
            request.state.max_body_size = 500 * 1024 * 1024  # 500MB
        
        response = await call_next(request)
        return response

app.add_middleware(LargeFileMiddleware)

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(upload.router, prefix="/api", tags=["Upload"])
app.include_router(detection.router, prefix="/api", tags=["Detection"])
app.include_router(pdf_embeddings.router, prefix="/api", tags=["PDF Embeddings"])
app.include_router(chat.router, prefix="/api", tags=["Chat"])
app.include_router(sql_rag.router, prefix="/api/rag", tags=["SQL RAG"])
app.include_router(ollama.router, prefix="/api/ollama", tags=["Ollama"])
app.include_router(system_prompt.router, prefix="/api", tags=["System Prompt"])
app.include_router(user_management.router, prefix="/api", tags=["User Management"])
app.include_router(database.router, prefix="/database", tags=["Database"])

# Mount static files for uploaded images
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

# Mount static files for processed PDF documents
DOCUMENTS_DIR = Path("documents")
DOCUMENTS_DIR.mkdir(exist_ok=True)
app.mount("/documents", StaticFiles(directory=str(DOCUMENTS_DIR)), name="documents")

# Mount the uploads-metadata.json file directly
from fastapi import Response
import json

@app.get("/uploads-metadata.json")
async def get_uploads_metadata():
    """Serve the uploads metadata JSON file."""
    try:
        metadata_file = Path("uploads-metadata.json")
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
            return metadata
        else:
            return {"uploads": []}
    except Exception as e:
        return {"uploads": [], "error": str(e)}

@app.get("/")
async def root():
    """Root endpoint that returns a welcome message."""
    return {
        "message": "Welcome to FastAPI Backend Service", 
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }