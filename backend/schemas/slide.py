from pydantic import BaseModel
from typing import Optional


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
