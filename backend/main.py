from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from dotenv import load_dotenv

from database import engine, Base
from models import Carousel, Slide, Generation
from routers import carousel_router, slide_router, generation_router, export_router

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Carousel Generator API",
    description="MVP API for Instagram carousel generation",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(carousel_router)
app.include_router(slide_router)
app.include_router(generation_router)
app.include_router(export_router)


@app.get("/")
def root():
    return {
        "status": "carousel generator running",
        "version": "1.0.0",
        "endpoints": {
            "carousels": "/carousels",
            "slides": "/carousels/{carousel_id}/slides",
            "generations": "/generations",
            "exports": "/exports",
            "docs": "/docs",
        },
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
