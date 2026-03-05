from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
import os
import logging

from database import get_db
from models import Carousel
from services.export_service import generate_carousel_images

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/exports", tags=["exports"])


class ExportRequest(BaseModel):
    carousel_id: int


@router.post("")
def export_carousel(
    request: ExportRequest,
    db: Session = Depends(get_db),
):
    """Export carousel slides as images in a ZIP archive"""
    # Verify carousel exists
    carousel = db.query(Carousel).filter(Carousel.id == request.carousel_id).first()
    if not carousel:
        raise HTTPException(status_code=404, detail="Carousel not found")

    try:
        # Generate images and ZIP
        zip_path = generate_carousel_images(request.carousel_id, db)

        # Return ZIP file
        return FileResponse(
            path=zip_path,
            filename=f"carousel_{request.carousel_id}_export.zip",
            media_type="application/zip",
        )

    except ValueError as e:
        logger.error(f"Export error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error during export: {str(e)}")
        raise HTTPException(status_code=500, detail="Export failed")
