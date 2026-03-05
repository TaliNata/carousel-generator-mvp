# API Testing Guide

Quick reference for testing the Carousel Generator API.

## Start the Server

### Option 1: Direct (requires local PostgreSQL)
```bash
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

### Option 2: Docker Compose (recommended)
```bash
docker-compose -f docker-compose.yaml up
```

API will be available at: `http://localhost:8000`

## Interactive API Docs

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Curl Examples

### 1. Check Health
```bash
curl http://localhost:8000/health
```

### 2. Create a Carousel
```bash
curl -X POST http://localhost:8000/carousels \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Product Launch",
    "source_type": "text",
    "source_payload": "Check out our new product! It has amazing features like AI-powered generation, fast processing, and beautiful templates.",
    "language": "en",
    "slides_count": 5
  }'
```

Response will include the carousel ID. Note it for next steps.

### 3. Get Carousel Details
```bash
curl http://localhost:8000/carousels/1
```

### 4. Trigger Generation (Async)
```bash
curl -X POST http://localhost:8000/generations \
  -H "Content-Type: application/json" \
  -d '{"carousel_id": 1}'
```

Response includes generation ID.

### 5. Check Generation Status
```bash
curl http://localhost:8000/generations/1
```

Expected progression:
1. `"status": "pending"` 
2. `"status": "processing"`
3. `"status": "completed"` with `result_json`

When complete, the carousel status should also be "ready".

### 6. Get Generated Slides
```bash
curl http://localhost:8000/carousels/1/slides
```

### 7. List All Carousels
```bash
curl http://localhost:8000/carousels?skip=0&limit=10
```

### 8. Update a Slide
```bash
curl -X PATCH http://localhost:8000/carousels/1/slides/1 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Title",
    "body": "This is the updated slide content",
    "footer": "Slide footer"
  }'
```

### 9. Update a Carousel
```bash
curl -X PATCH http://localhost:8000/carousels/1 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Product Launch",
    "language": "es",
    "slides_count": 10
  }'
```

## Testing Workflow

1. **Create carousel** - Get carousel ID from response
2. **Trigger generation** - Get generation ID from response
3. **Poll generation status** - Check until status is "completed"
4. **Get slides** - Download generated slides
5. **Edit slides** - Customize content as needed

## Mock vs Real Generation

### Without OpenAI API Key
- Generation will use mock data
- Useful for testing the workflow
- Slide data is templated but valid

### With OpenAI API Key
- Set `OPENAI_API_KEY` in `.env`
- Generation uses ChatGPT 3.5 Turbo
- Unique, AI-generated content

## Troubleshooting

### Database Connection Error
```
Error: could not connect to server
```
- Make sure PostgreSQL is running
- Check `DATABASE_URL` in `.env`
- If using Docker: `docker-compose up` first

### OpenAI API Error
- Check `OPENAI_API_KEY` is valid
- System will fallback to mock generation
- Check logs for rate limiting

### Carousel Not Found (404)
- Make sure carousel ID exists
- Check ID from create response
- Use GET /carousels to list all

## Performance Notes

- Generation typically takes 2-5 seconds
- Background tasks run asynchronously
- Multiple carousels can be generated in parallel
- Mock generation is instant for testing
