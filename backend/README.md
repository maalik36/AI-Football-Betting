# AI American Football Betting Backend

FastAPI backend for AI-powered American football betting predictions using Google Gemini API.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Setup

1. **Navigate to backend directory:**

   **On macOS/Linux:**
   ```bash
   cd backend
   ```

   **On Windows:**
   ```cmd
   cd backend
   ```

2. **Create virtual environment:**

   **On macOS/Linux:**
   ```bash
   python -m venv venv
   ```

   **On Windows:**
   ```cmd
   python -m venv venv
   ```

3. **Activate virtual environment:**

   **On macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```

   **On Windows (Command Prompt):**
   ```cmd
   venv\Scripts\activate
   ```

   **On Windows (PowerShell):**
   ```powershell
   venv\Scripts\Activate.ps1
   ```

4. **Install dependencies:**

   **On macOS/Linux:**
   ```bash
   pip install -r requirements.txt
   ```

   **On Windows:**
   ```cmd
   pip install -r requirements.txt
   ```

5. **Set up environment variables:**

   **On macOS/Linux:**
   ```bash
   cp env.example .env
   ```

   **On Windows:**
   ```cmd
   copy env.example .env
   ```

6. **Edit .env file with environment variables provided from team chat:**

   **On macOS/Linux:**
   ```bash
   # Use any text editor
   nano .env
   # or
   vim .env
   ```

   **On Windows:**
   ```cmd
   # Use Notepad
   notepad .env
   # or use any text editor like VS Code, Notepad++, etc.
   ```

   Replace the placeholder values with actual values from team:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

## Running the Server

**Development mode (with auto-reload):**

**On macOS/Linux:**
```bash
python run.py
```

**On Windows:**
```cmd
python run.py
```

**Production mode:**

**On macOS/Linux:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**On Windows:**
```cmd
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**With specific host/port:**

**On macOS/Linux:**
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

**On Windows:**
```cmd
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

## Accessing the API

- **API Base URL:** `http://localhost:8000`
- **Interactive Docs:** `http://localhost:8000/docs`
- **Alternative Docs:** `http://localhost:8000/redoc`

## API Endpoints

- `GET /` - API info
- `GET /health` - Health check
- `GET /api/v1/matches` - Get American football matches
- `GET /api/v1/predictions` - Get predictions
- `POST /api/v1/predict` - Get AI prediction for match
- `POST /api/v1/predict-simple` - Get simple prediction
- `GET /api/v1/team-form/{team_name}` - Get team form analysis

## Example API Usage

**Get simple prediction:**

**On macOS/Linux:**
```bash
curl -X POST "http://localhost:8000/api/v1/predict-simple" \
     -H "Content-Type: application/json" \
     -d '"Kansas City Chiefs vs Buffalo Bills"'
```

**On Windows (PowerShell):**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/predict-simple" `
     -Method POST `
     -Headers @{"Content-Type"="application/json"} `
     -Body '"Kansas City Chiefs vs Buffalo Bills"'
```

**On Windows (Command Prompt):**
```cmd
curl -X POST "http://localhost:8000/api/v1/predict-simple" -H "Content-Type: application/json" -d "Kansas City Chiefs vs Buffalo Bills"
```

**Get detailed prediction:**

**On macOS/Linux:**
```bash
curl -X POST "http://localhost:8000/api/v1/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "id": "1",
       "home_team": "Kansas City Chiefs",
       "away_team": "Buffalo Bills",
       "date": "2024-01-15",
       "league": "NFL"
     }'
```

**On Windows (PowerShell):**
```powershell
$body = @{
    id = "1"
    home_team = "Kansas City Chiefs"
    away_team = "Buffalo Bills"
    date = "2024-01-15"
    league = "NFL"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/predict" `
     -Method POST `
     -Headers @{"Content-Type"="application/json"} `
     -Body $body
```

**Get team form:**

**On macOS/Linux:**
```bash
curl "http://localhost:8000/api/v1/team-form/Kansas%20City%20Chiefs"
```

**On Windows:**
```cmd
curl "http://localhost:8000/api/v1/team-form/Kansas%%20City%%20Chiefs"
```

## Getting Environment Variables

**Copy the environment variables provided in team chat:**
- The team will provide the necessary API keys and configuration values
- Replace the placeholder values in `.env` file with the actual values from team chat
- Do not commit the actual API keys to version control

## Project Structure

```
backend/
├── app/
│   ├── api/                    # API routes
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── config/                 # Configuration
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── models/                 # Data models
│   │   ├── __init__.py
│   │   └── schemas.py
│   ├── services/               # Business logic & AI services
│   │   ├── __init__.py
│   │   ├── gemini_client.py    # Gemini API client
│   │   └── prediction_service.py # Prediction business logic
│   ├── __init__.py
│   └── main.py                 # FastAPI app
├── venv/                       # Virtual environment (created during setup)
├── requirements.txt            # Python dependencies
├── run.py                      # Entry point
├── env.example                 # Environment template
└── README.md                   # This file
```

## Troubleshooting

**Port already in use:**

**On macOS/Linux:**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

**On Windows:**
```cmd
# Find process using port 8000
netstat -ano | findstr :8000

# Kill process by PID (replace XXXX with actual PID)
taskkill /PID XXXX /F
```

**Virtual environment not activated:**
- Make sure you see `(venv)` in your terminal prompt
- If not, run: 
  - **macOS/Linux:** `source venv/bin/activate`
  - **Windows (Command Prompt):** `venv\Scripts\activate`
  - **Windows (PowerShell):** `venv\Scripts\Activate.ps1`

**API key issues:**
- Ensure your `.env` file exists and contains the correct API key from team chat
- Check that the key is valid in Google AI Studio

**Dependencies not found:**

**On macOS/Linux:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**On Windows:**
```cmd
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**Windows-specific issues:**

**PowerShell execution policy:**
```powershell
# If you get execution policy errors, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Path issues:**
- Make sure Python is in your system PATH
- Use `python --version` to verify Python is accessible

**File permissions:**
- Run Command Prompt or PowerShell as Administrator if you encounter permission issues

## Development

**Deactivate virtual environment when done:**

**On macOS/Linux:**
```bash
deactivate
```

**On Windows:**
```cmd
deactivate
```

**Update dependencies:**

**On macOS/Linux:**
```bash
pip freeze > requirements.txt
```

**On Windows:**
```cmd
pip freeze > requirements.txt
```

## Gemini API Usage

The backend uses Google's Gemini API for AI-powered football predictions. Make sure to:
1. Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Add it to your `.env` file
3. The API will analyze matches and provide betting predictions 