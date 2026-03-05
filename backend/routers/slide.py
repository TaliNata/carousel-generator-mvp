from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Slide, Carousel
from schemas import SlideResponse, SlideUpdate

router = APIRouter(prefix="/carousels", tags=["slides"])


@router.get("/{carousel_id}/slides", response_model=List[SlideResponse])
def get_carousel_slides(carousel_id: int, db: Session = Depends(get_db)):
    """Get all slides for a carousel"""
    carousel = db.query(Carousel).filter(Carousel.id == carousel_id).first()
    if not carousel:
        raise HTTPException(status_code=404, detail="Carousel not found")

    slides = (
        db.query(Slide)
        .filter(Slide.carousel_id == carousel_id)
        .order_by(Slide.order)
        .all()
    )
    return slides


@router.patch("/{carousel_id}/slides/{slide_id}", response_model=SlideResponse)
def update_slide(
    carousel_id: int,
    slide_id: int,
    slide_update: SlideUpdate,
    db: Session = Depends(get_db),
):
    """Update a specific slide in a carousel"""
    carousel = db.query(Carousel).filter(Carousel.id == carousel_id).first()
    if not carousel:
        raise HTTPException(status_code=404, detail="Carousel not found")

    slide = (
        db.query(Slide)
        .filter((Slide.id == slide_id) & (Slide.carousel_id == carousel_id))
        .first()
    )
    if not slide:
        raise HTTPException(status_code=404, detail="Slide not found")

    update_data = slide_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(slide, field, value)

    db.add(slide)
    db.commit()
    db.refresh(slide)
    return slide
