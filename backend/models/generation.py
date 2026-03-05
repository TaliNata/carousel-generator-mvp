from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base
import enum


class GenerationStatus(str, enum.Enum):
    pending = "pending"
    processing = "processing"
    completed = "completed"
    failed = "failed"


class Generation(Base):
    __tablename__ = "generations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    carousel_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("carousels.id"), nullable=False
    )
    status: Mapped[GenerationStatus] = mapped_column(
        Enum(GenerationStatus), default=GenerationStatus.pending
    )
    result_json: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )  # JSON as string
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    carousel = relationship("Carousel", back_populates="generations")
