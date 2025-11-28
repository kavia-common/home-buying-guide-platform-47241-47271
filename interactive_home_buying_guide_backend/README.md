# Interactive Home Buying Guide Backend (Flask)

Runs a simple Flask API serving guide steps, resources, and progress using in-memory storage.

## Endpoints
- GET /api/steps
- GET /api/steps/<id>
- POST /api/steps/<id>/checklist/<item_id>/toggle
- GET /api/resources
- GET /api/progress

## Dev Run
- Default port: 3001 (set BACKEND_PORT to override)
- CORS: allows http://localhost:3000 by default (override with FRONTEND_ORIGIN)

Install and run:
pip install -r requirements.txt
python run.py
