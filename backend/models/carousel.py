from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.types import String as StringType
from database import Base
import enum


class CarouselStatus(str, enum.Enum):
    draft = "draft"
    generating = "generating"
    ready = "ready"
    failed = "failed"


class Carousel(Base):
    __tablename__ = "carousels"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    source_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # "text", "url", etc.
    source_payload: Mapped[str] = mapped_column(Text, nullable=False)  # JSON as string
    language: Mapped[str] = mapped_column(String(10), default="en")
    slides_count: Mapped[int] = mapped_column(Integer, default=5)
    status: Mapped[CarouselStatus] = mapped_column(
        Enum(CarouselStatus), default=CarouselStatus.draft
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    slides = relationship(
        "Slide", back_populates="carousel", cascade="all, delete-orphan"
    )
    generations = relationship(
        "Generation", back_populates="carousel", cascade="all, delete-orphan"
    )
