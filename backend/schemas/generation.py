from pydantic import BaseModel
from typing import Optional
from datetime import datetime


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
    slides: list[SlideGenerationData]
