"""
Main FastAPI application for Medical Research Agent.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.core.config import settings
from app.api.routes import router as api_router


# Configure logging
logging.basicConfig(
    level=logging.INFO if not settings.debug else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("Starting Medical Research Agent API...")
    logger.info(f"Version: {settings.app_version}")
    logger.info(f"Model: {settings.model_name}")
    
    # Verify configuration
    if not settings.google_api_key:
        logger.warning("Google API key not configured!")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Medical Research Agent API...")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="""
    Medical Research Agent API
    
    An AI-powered medical research assistant that can:
    - Search PubMed for peer-reviewed medical literature
    - Check drug interactions and adverse events
    - Answer clinical questions using trusted medical sources
    - Provide comprehensive, evidence-based answers
    
    Built with LangGraph, Gemini, and multiple medical data sources.
    """,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router, prefix="/api/v1", tags=["agent"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "docs": "/docs"
    }


@app.get("/ping")
async def ping():
    """Simple health check."""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
