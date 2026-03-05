# Carousel Generator MVP

Mini-product that generates Instagram carousel slides using an LLM.

<img width="1860" height="871" alt="Снимок экрана 2026-03-05 160446" src="https://github.com/user-attachments/assets/b7b589ae-eada-48ed-bb87-9de0195cd561" />

## Tech stack

**Backend:**
- FastAPI
- SQLAlchemy
- OpenRouter (LLM)
- Pillow (image export)

**Frontend:**
- Nuxt 4
- Vue 3

## Features

- Create carousel from text
- Generate slides using LLM
- Edit slides in the editor
- Export slides as PNG images in a ZIP archive

## Architecture

```
User → Nuxt frontend
  ↓
FastAPI backend
  ↓
OpenRouter LLM generates slides
  ↓
Slides saved in database
  ↓
Editor allows editing
  ↓
Export service renders PNG slides and returns ZIP
```

## Running the project

### Backend

```bash
cd backend
pip install -r requirements.txt
```

Create `.env` file:

```
OPENROUTER_API_KEY=your_api_key_here
```

Run server:

```bash
uvicorn main:app --reload
```

API docs available at:
```
http://127.0.0.1:8000/docs
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open browser:
```
http://localhost:3000
```

## Main API endpoints

- `POST /carousels` - Create carousel
- `POST /generations` - Generate slides
- `GET /carousels/{id}/slides` - Get carousel slides
- `POST /exports` - Export slides to ZIP

## Simplifications for MVP

- Simplified LLM prompt
- Image export implemented using Pillow
- Minimal UI
- No authentication

## AI tools used

GitHub Copilot

## Testing

To test the API without OpenAI API key, the system uses mock generation.

Example workflow:
```bash
# Create carousel
curl -X POST http://localhost:8000/carousels -d {...}

# Trigger generation
curl -X POST http://localhost:8000/generations -d '{"carousel_id": 1}'

# Check status
curl http://localhost:8000/generations/1

# Get slides
curl http://localhost:8000/carousels/1/slides
```

## Roadmap

### Phase 2
- [ ] Image generation
- [ ] Better LLM prompting
- [ ] Analytics & usage tracking
- [ ] Rate limiting

### Phase 3
- [ ] Frontend UI
- [ ] User authentication
- [ ] Multiple template styles
- [ ] Scheduling/publishing

### Production
- [ ] Comprehensive testing
- [ ] API authentication (JWT)
- [ ] Database migrations
- [ ] Monitoring & logging
- [ ] Docker deployment
- [ ] CI/CD pipeline

## License

MIT
