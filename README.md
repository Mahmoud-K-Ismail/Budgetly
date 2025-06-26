# NYUAD Smart Budgeting Assistant

A full-stack personal budgeting assistant designed specifically for NYUAD students to track and manage their monthly stipends. Built with FastAPI backend and React frontend.

## 🚀 Features

### Backend Features
- **User Profile Management**: Set stipend, savings goals, and budget cycle
- **Expense Tracking**: Add and categorize expenses
- **Budget Summary**: Real-time budget calculations and remaining amounts
- **Smart Recommendations**: AI-powered financial advice
- **Reports**: Export expense data in CSV/JSON format

### Frontend Features
- **Dashboard**: Overview of budget status and spending patterns
- **Expense Entry**: Easy form to add new expenses
- **History View**: Complete expense history with filtering
- **Visualizations**: Charts showing spending breakdown
- **Recommendations Panel**: Financial tips and advice

## 🛠 Tech Stack

### Backend
- **Python 3.10+**
- **FastAPI** - Modern web framework
- **SQLAlchemy** - Database ORM
- **SQLite** - Database (PostgreSQL for production)
- **Pydantic** - Data validation
- **Pandas** - Data processing

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool
- **TailwindCSS** - Styling
- **Axios** - HTTP client
- **Recharts** - Data visualization

## 📁 Project Structure

```
NYUAD-Budgetly/
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── users.py
│   │   ├── expenses.py
│   │   └── summary.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── calculations.py
│   │   └── recommendations.py
│   └── tests/
│       └── test_main.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── api/
│   │   └── App.jsx
│   ├── package.json
│   └── tailwind.config.js
├── .env.example
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the server:**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```

The app will be available at `http://localhost:5173`

## 📖 API Documentation

Once the backend is running, visit:
- **Interactive API Docs**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Key Endpoints

- `POST /user` - Create user profile
- `POST /expenses` - Add expense
- `GET /summary/{user_id}` - Get budget summary
- `GET /recommendations/{user_id}` - Get financial recommendations
- `GET /report/{user_id}` - Export expense report

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 🎯 Example User Flow

1. **Setup Profile**: Enter stipend amount, savings goal, and budget cycle start date
2. **Add Expenses**: Log daily expenses with categories and descriptions
3. **Monitor Budget**: View real-time budget summary and spending breakdown
4. **Get Insights**: Receive personalized financial recommendations
5. **Track Progress**: Export reports and analyze spending patterns

## 🔧 Environment Variables

Copy `.env.example` to `.env` and configure:

```env
DATABASE_URL=sqlite:///./budgetly.db
SECRET_KEY=your-secret-key-here
DEBUG=True
```

## 🚀 Deployment

### Backend (Render)
- Connect GitHub repository
- Set build command: `pip install -r requirements.txt`
- Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Frontend (Vercel)
- Connect GitHub repository
- Set build command: `npm run build`
- Set output directory: `dist`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
- Create an issue on GitHub
- Contact: [Your Email]

---

Built with ❤️ for NYUAD Students 