import json
import os
import requests
from typing import Optional
from sqlalchemy.orm import Session
import logging

from models import Generation, Carousel, Slide, GenerationStatus, CarouselStatus
from schemas import GenerationResult

logger = logging.getLogger(__name__)


def generate_carousel_content(generation_id: int, carousel_id: int, db: Session):
    """
    Background task to generate carousel slides using LLM.

    This function:
    1. Fetches the carousel and generation records
    2. Calls the LLM to generate slide content
    3. Creates Slide records for each generated slide
    4. Updates the carousel status to "ready"
    5. Updates the generation status to "completed"
    """
    try:
        # Fetch records
        carousel = db.query(Carousel).filter(Carousel.id == carousel_id).first()
        generation = db.query(Generation).filter(Generation.id == generation_id).first()

        if not carousel or not generation:
            logger.error(f"Carousel or Generation not found")
            return

        # Update generation status to processing
        generation.status = GenerationStatus.processing
        db.add(generation)
        db.commit()

        # Call LLM to generate slides
        slides_data = call_llm_for_generation(
            source_text=str(carousel.source_payload),
            language=str(carousel.language),
            slides_count=int(carousel.slides_count),
        )

        # Parse and validate response
        result = GenerationResult(**slides_data)

        # Create Slide records
        for order, slide_data in enumerate(result.slides, start=1):
            slide = Slide(
                carousel_id=carousel_id,
                order=order,
                title=slide_data.title,
                body=slide_data.body,
                footer=None,  # Can be added later by user
            )
            db.add(slide)

        # Update carousel status to ready
        carousel.status = CarouselStatus.ready
        db.add(carousel)

        # Update generation with result and mark as completed
        generation.status = GenerationStatus.completed
        generation.result_json = json.dumps(slides_data)
        db.add(generation)

        db.commit()
        logger.info(f"Generation {generation_id} completed successfully")

    except Exception as e:
        logger.error(f"Error during generation {generation_id}: {str(e)}")
        # Update status to failed
        try:
            generation = (
                db.query(Generation).filter(Generation.id == generation_id).first()
            )
            if generation:
                generation.status = GenerationStatus.failed
                db.add(generation)

            carousel = db.query(Carousel).filter(Carousel.id == carousel_id).first()
            if carousel:
                carousel.status = CarouselStatus.failed
                db.add(carousel)

            db.commit()
        except Exception as rollback_error:
            logger.error(f"Error during rollback: {str(rollback_error)}")
            db.rollback()


def call_llm_for_generation(source_text: str, language: str, slides_count: int) -> dict:
    """
    Call OpenRouter API to generate carousel slides.

    Args:
        source_text: The source content to generate slides from
        language: Target language for the slides
        slides_count: Number of slides to generate

    Returns:
        Dictionary with structure: {"slides": [{"title": "...", "body": "..."}]}

    Raises:
        ValueError: If API response is invalid or missing OPENROUTER_API_KEY
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not set in environment variables")

    url = "https://openrouter.ai/api/v1/chat/completions"

    prompt = f"""Convert the following text into an Instagram carousel.

Rules:
- Create exactly {slides_count} slides
- Each slide must contain:
  title (short, max 50 chars)
  body (2-3 sentences, max 200 chars)

Return valid JSON only.
Do not include explanations.

JSON format:
{{
  "slides": [
    {{"title": "...", "body": "..."}}
  ]
}}

Text:
{source_text}

Language:
{language}"""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "openai/gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()

        response_data = response.json()
        content = (
            response_data.get("choices", [{}])[0].get("message", {}).get("content")
        )

        if not content:
            raise ValueError("Empty response from OpenRouter API")

        # Extract JSON from response
        json_start = content.find("{")
        json_end = content.rfind("}") + 1

        if json_start == -1 or json_end <= json_start:
            raise ValueError(f"Could not extract JSON from LLM response: {content}")

        json_str = content[json_start:json_end]
        result = json.loads(json_str)

        logger.info(f"Successfully generated {len(result.get('slides', []))} slides")
        return result

    except requests.RequestException as e:
        logger.error(f"OpenRouter API request failed: {str(e)}")
        raise ValueError(f"OpenRouter API error: {str(e)}")
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON from LLM response: {str(e)}")
        raise ValueError(f"Invalid JSON in LLM response: {str(e)}")
