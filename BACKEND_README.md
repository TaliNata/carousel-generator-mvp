# Carousel Generator Backend

MVP FastAPI backend for Instagram carousel generation using AI.

## Setup & Installation

### Prerequisites
- Python 3.8+
- PostgreSQL running locally
- OpenAI API key (optional for testing with mock generation)

### Installation Steps

1. **Copy environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Update .env with your configuration:**
   ```
   DATABASE_URL=postgresql://postgres:postgres@localhost:5432/carousel_generator
   OPENAI_API_KEY=your_secret_key_here
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create PostgreSQL database:**
   ```bash
   createdb carousel_generator
   ```

5. **Run the server:**
   ```bash
   uvicorn backend.main:app --reload
   ```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Project Structure

```
backend/
├── main.py              # FastAPI app setup, routers
├── database.py          # SQLAlchemy configuration
├── models/              # Database models
│   ├── carousel.py      # Carousel model
│   ├── slide.py         # Slide model
│   └── generation.py    # Generation task model
├── schemas/             # Pydantic request/response schemas
│   ├── carousel.py
│   ├── slide.py
│   └── generation.py
├── routers/             # API route handlers
│   ├── carousel.py      # Carousel endpoints
│   ├── slide.py         # Slide endpoints
│   └── generation.py    # Generation endpoints
└── services/            # Business logic
    └── generation_service.py  # LLM integration
```

## API Endpoints

### Carousels

- **GET `/carousels`** - List all carousels
  - Query params: `skip`, `limit`
  
- **POST `/carousels`** - Create new carousel
  - Request body:
    ```json
    {
      "title": "My Carousel",
      "source_type": "text",
      "source_payload": "Your content here...",
      "language": "en",
      "slides_count": 5
    }
    ```

- **GET `/carousels/{id}`** - Get carousel by ID

- **PATCH `/carousels/{id}`** - Update carousel
  - Request body: (partial update)
    ```json
    {
      "title": "Updated Title",
      "language": "es",
      "slides_count": 10
    }
    ```

### Slides

- **GET `/carousels/{carousel_id}/slides`** - Get all slides for a carousel

- **PATCH `/carousels/{carousel_id}/slides/{slide_id}`** - Update a slide
  - Request body:
    ```json
    {
      "title": "Updated Title",
      "body": "Updated content",
      "footer": "Optional footer"
    }
    ```

### Generations

- **POST `/generations`** - Create new generation task (async)
  - Request body:
    ```json
    {
      "carousel_id": 1
    }
    ```
  - Response includes generation ID to track progress

- **GET `/generations/{id}`** - Get generation status and result

## Usage Example

1. **Create a carousel:**
   ```bash
   curl -X POST http://localhost:8000/carousels \
     -H "Content-Type: application/json" \
     -d '{
       "title": "My First Carousel",
       "source_type": "text",
       "source_payload": "Here is some content about my product...",
       "language": "en",
       "slides_count": 5
     }'
   ```

2. **Trigger generation:**
   ```bash
   curl -X POST http://localhost:8000/generations \
     -H "Content-Type: application/json" \
     -d '{"carousel_id": 1}'
   ```

3. **Check generation status:**
   ```bash
   curl http://localhost:8000/generations/1
   ```

4. **Get generated slides:**
   ```bash
   curl http://localhost:8000/carousels/1/slides
   ```

## Features

- ✅ Database models with SQLAlchemy & PostgreSQL
- ✅ RESTful API with FastAPI
- ✅ Async background tasks for content generation
- ✅ LLM integration (OpenAI) with mock fallback
- ✅ CRUD operations for carousels and slides
- ✅ Generation tracking with status updates
- ✅ Multi-language support

## Development Notes

### Mock Generation
If you don't have an OpenAI API key, the system falls back to mock slide generation. This is useful for development and testing.

### Async Tasks
The generation process runs in the background using FastAPI's BackgroundTasks. The carousel status will update from:
1. `draft` → `generating` (when task starts)
2. `generating` → `ready` (when generation completes)
3. Or `generating` → `failed` (if error occurs)

### Database Migrations
Currently, tables are created automatically on app startup. For production, consider using Alembic for migrations.

## Next Steps for Production

- [ ] Add authentication (JWT tokens)
- [ ] Add image generation capability
- [ ] Implement database migrations (Alembic)
- [ ] Add rate limiting
- [ ] Add comprehensive error handling
- [ ] Add logging configuration
- [ ] Add caching layer
- [ ] Dockerize the application
- [ ] Add comprehensive tests
- [ ] Add input validation & sanitization
