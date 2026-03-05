from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class SlideBase(BaseModel):
    title: str
    body: str
    footer: Optional[str] = None


class SlideCreate(SlideBase):
    order: int


class SlideUpdate(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None
    footer: Optional[str] = None


class SlideResponse(SlideBase):
    id: int
    carousel_id: int
    order: int

    class Config:
        from_attributes = True


class CarouselBase(BaseModel):
    title: str
    source_type: str
    source_payload: str
    language: str = "en"
    slides_count: int = 5


class CarouselCreate(CarouselBase):
    pass


class CarouselUpdate(BaseModel):
    title: Optional[str] = None
    language: Optional[str] = None
    slides_count: Optional[int] = None


class CarouselResponse(CarouselBase):
    id: int
    status: str
    created_at: datetime
    slides: List[SlideResponse] = []

    class Config:
        from_attributes = True


class GenerationCreate(BaseModel):
    carousel_id: int


class GenerationResponse(BaseModel):
    id: int
    carousel_id: int
    status: str
    result_json: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class SlideGenerationData(BaseModel):
    title: str
    body: str


class GenerationResult(BaseModel):
    slides: List[SlideGenerationData]
