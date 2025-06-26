# Manual Setup Guide

If you prefer to start the backend and frontend separately, follow these steps:

## Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Start the server:**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Test the API:**
   ```bash
   python test_api.py
   ```

The backend will be available at:
- API: http://localhost:8000
- Documentation: http://localhost:8000/docs

## Frontend Setup

1. **Open a new terminal and navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

The frontend will be available at:
- Application: http://localhost:5173

## Troubleshooting

### Backend Issues

**Pandas Installation Error:**
- The requirements.txt has been updated to remove pandas dependency
- CSV export functionality now works without pandas

**Pydantic Schema Error:**
- Fixed the field name clashing issue in schemas.py

**Missing Dependencies:**
- Make sure you're in the virtual environment: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`

### Frontend Issues

**React Syntax Error:**
- Fixed the main.jsx file with proper closing tags

**Node Modules Issues:**
- Delete node_modules and reinstall: `rm -rf node_modules && npm install`

**Port Already in Use:**
- Change the port in vite.config.js or kill the process using the port

## Quick Commands

**Start both servers (recommended):**
```bash
./start_simple.sh
```

**Start backend only:**
```bash
cd backend && source venv/bin/activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Start frontend only:**
```bash
cd frontend && npm run dev
```

## Environment Variables

Copy the example environment file:
```bash
cp env.example .env
```

Edit `.env` to configure:
- Database URL
- Secret key
- Debug mode
- CORS settings 