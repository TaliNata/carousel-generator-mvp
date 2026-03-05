from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base


class Slide(Base):
    __tablename__ = "slides"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    carousel_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("carousels.id"), nullable=False
    )
    order: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    footer: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Relationships
    carousel = relationship("Carousel", back_populates="slides")
