from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
import json

from database import get_db
from models import Generation, Carousel, CarouselStatus
from schemas import GenerationCreate, GenerationResponse
from services.generation_service import generate_carousel_content

router = APIRouter(prefix="/generations", tags=["generations"])


@router.post("", response_model=GenerationResponse, status_code=201)
def create_generation(
    generation: GenerationCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """Create a new generation task (async)"""
    carousel = db.query(Carousel).filter(Carousel.id == generation.carousel_id).first()
    if not carousel:
        raise HTTPException(status_code=404, detail="Carousel not found")

    # Create generation record
    db_generation = Generation(carousel_id=generation.carousel_id)
    db.add(db_generation)
    db.commit()
    db.refresh(db_generation)

    # Update carousel status to generating
    carousel.status = CarouselStatus.generating
    db.add(carousel)
    db.commit()

    # Get the IDs after refresh
    gen_id = db_generation.id
    car_id = carousel.id

    # Add async task to generate content
    background_tasks.add_task(generate_carousel_content, gen_id, car_id, db)

    return db_generation


@router.get("/{generation_id}", response_model=GenerationResponse)
def get_generation(generation_id: int, db: Session = Depends(get_db)):
    """Get generation status and result"""
    generation = db.query(Generation).filter(Generation.id == generation_id).first()
    if not generation:
        raise HTTPException(status_code=404, detail="Generation not found")
    return generation
