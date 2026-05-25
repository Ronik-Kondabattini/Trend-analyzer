# 📈 TrendPulse — Trend Analyzer

A Django app that analyzes any topic and instantly returns:

- 📊 Trend metrics
- 🎥 YouTube suggestions
- 💡 Content ideas

### ✨ Core Features
- Topic analysis with trend score & metrics
- YouTube video suggestions
- Content idea generator
- Save ideas + search history
- User dashboard with stats
- Auth system + admin panel

---

## 🧱 Repository Structure

The repository is organized into distinct logical components for clear separation of concerns:

```
Trend-analyzer/
├── backend/               # Main Django Application
│   ├── core/              # Main app (models, views, business logic)
│   ├── django_project/    # Core config (settings, URLs)
│   ├── manage.py          # Django management script
│   └── requirements.txt   # Python dependencies
├── frontend/              # Frontend code (Placeholder for future decoupled UI)
├── docs/                  # Project documentation (API, Contributing guidelines)
├── tests/                 # Automated testing suite
├── configs/               # Environment & deployment configurations
├── .gitignore             # Ignored files (including .env)
├── LICENSE                # MIT License
└── README.md              # Project overview (this file)
```

👉 **Everything important lives in `backend/core/` (this is what devs care about)**

---

## 🚀 Quick Start (Backend)

Follow these steps to run the Django backend locally:

```bash
# 1. Clone the repository
git clone https://github.com/Ronik-Kondabattini/Trend-analyzer.git
cd Trend-analyzer/backend

# 2. Set up virtual environment
python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up the database (requires MySQL or compatible DB)
# Create a database named 'trendpulse' in your MySQL server
# cp .env.example .env (Ensure you configure your credentials here)
python manage.py migrate
python manage.py seed

# 5. Run the development server
python manage.py runserver
```

👉 **App URL**: `http://localhost:8000`  
👉 **Demo Credentials**: `demo@example.com` / `password123`

---

## 🔗 Main Routes

- `/dashboard/` → User Dashboard
- `/api/analyze/` → Analyze topic
- `/api/history/` → Search History
- `/api/saved-ideas/` → Saved Content Ideas
- `/admin/` → Admin Panel

---

## 🛠️ Technology Stack

- **Backend**: Django, Python
- **Database**: MySQL
- **Frontend**: HTML, CSS, JavaScript (Currently bundled via Django templates)

---

## 📚 Documentation

Detailed documentation is available in the `docs/` directory:
- [API Documentation](docs/API_DOCUMENTATION.md)
- [Contributing Guidelines](docs/CONTRIBUTING.md)

---

## 📝 License

This project is licensed under the [MIT License](LICENSE).
