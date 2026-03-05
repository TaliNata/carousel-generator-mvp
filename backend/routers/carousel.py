from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Carousel, CarouselStatus
from schemas import CarouselCreate, CarouselUpdate, CarouselResponse

router = APIRouter(prefix="/carousels", tags=["carousels"])


@router.get("", response_model=List[CarouselResponse])
def get_carousels(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Get all carousels with pagination"""
    carousels = db.query(Carousel).offset(skip).limit(limit).all()
    return carousels


@router.post("", response_model=CarouselResponse, status_code=201)
def create_carousel(carousel: CarouselCreate, db: Session = Depends(get_db)):
    """Create a new carousel"""
    db_carousel = Carousel(**carousel.dict())
    db.add(db_carousel)
    db.commit()
    db.refresh(db_carousel)
    return db_carousel


@router.get("/{carousel_id}", response_model=CarouselResponse)
def get_carousel(carousel_id: int, db: Session = Depends(get_db)):
    """Get a specific carousel by ID"""
    carousel = db.query(Carousel).filter(Carousel.id == carousel_id).first()
    if not carousel:
        raise HTTPException(status_code=404, detail="Carousel not found")
    return carousel


@router.patch("/{carousel_id}", response_model=CarouselResponse)
def update_carousel(
    carousel_id: int, carousel_update: CarouselUpdate, db: Session = Depends(get_db)
):
    """Update a carousel"""
    carousel = db.query(Carousel).filter(Carousel.id == carousel_id).first()
    if not carousel:
        raise HTTPException(status_code=404, detail="Carousel not found")

    update_data = carousel_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(carousel, field, value)

    db.add(carousel)
    db.commit()
    db.refresh(carousel)
    return carousel
