import os
import tempfile
import zipfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from sqlalchemy.orm import Session
import logging

from models import Carousel, Slide

logger = logging.getLogger(__name__)

# Image dimensions
IMAGE_WIDTH = 1080
IMAGE_HEIGHT = 1350
BACKGROUND_COLOR = (255, 255, 255)
TEXT_COLOR = (0, 0, 0)


def generate_carousel_images(carousel_id: int, db: Session) -> str:
    """
    Generate images for all slides in a carousel and create a ZIP archive.
    
    Args:
        carousel_id: ID of the carousel
        db: Database session
    
    Returns:
        Path to the generated ZIP file
    
    Raises:
        ValueError: If carousel or slides not found
    """
    # Load carousel and slides
    carousel = db.query(Carousel).filter(Carousel.id == carousel_id).first()
    if not carousel:
        raise ValueError(f"Carousel {carousel_id} not found")
    
    slides = (
        db.query(Slide)
        .filter(Slide.carousel_id == carousel_id)
        .order_by(Slide.order)
        .all()
    )
    
    if not slides:
        raise ValueError(f"No slides found for carousel {carousel_id}")
    
    # Create temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Generate images for each slide
        for slide in slides:
            image_path = temp_path / f"slide_{slide.order:02d}.png"
            create_slide_image(
                title=slide.title,
                body=slide.body,
                output_path=str(image_path)
            )
            logger.info(f"Generated image: {image_path}")
        
        # Create ZIP archive
        zip_filename = f"carousel_{carousel_id}_export.zip"
        zip_path = temp_path / zip_filename
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for image_file in sorted(temp_path.glob("slide_*.png")):
                zipf.write(image_file, arcname=image_file.name)
                logger.info(f"Added to ZIP: {image_file.name}")
        
        # Copy ZIP to a persistent location
        exports_dir = Path("exports")
        exports_dir.mkdir(exist_ok=True)
        final_zip_path = exports_dir / zip_filename
        
        with open(zip_path, 'rb') as f:
            with open(final_zip_path, 'wb') as out:
                out.write(f.read())
        
        logger.info(f"Created export ZIP: {final_zip_path}")
        return str(final_zip_path)


def create_slide_image(title: str, body: str, output_path: str):
    """
    Create a single slide image with title and body text.
    
    Args:
        title: Slide title
        body: Slide body text
        output_path: Path to save the image
    """
    # Create new image
    image = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(image)
    
    # Try to use a better font if available, otherwise use default
    try:
        title_font = ImageFont.truetype("arial.ttf", size=60)
        body_font = ImageFont.truetype("arial.ttf", size=40)
    except (OSError, IOError):
        # Fallback to default font
        title_font = ImageFont.load_default()
        body_font = ImageFont.load_default()
    
    # Calculate positions
    margin = 60
    title_y = 200
    body_y = 600
    max_width = IMAGE_WIDTH - 2 * margin
    
    # Draw title
    draw.text(
        (margin, title_y),
        title,
        fill=TEXT_COLOR,
        font=title_font,
        anchor="lm",
    )
    
    # Draw body (wrapped) with fallback text color check
    draw.multiline_text(
        (margin, body_y),
        body,
        fill=TEXT_COLOR,
        font=body_font,
        spacing=20
    )
    
    # Save image
    image.save(output_path)
