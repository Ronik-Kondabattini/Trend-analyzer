📈 TrendPulse — Trend Analyzer

A Django app that analyzes any topic and instantly returns:

📊 Trend metrics
🎥 YouTube suggestions
💡 Content ideas
✨ Core Features
Topic analysis with trend score & metrics
YouTube video suggestions
Content idea generator
Save ideas + search history
User dashboard with stats
Auth system + admin panel


🧱 Project Structure
django_project/
├── django_project/        # Core config (settings, URLs)
├── core/                  # Main app (all logic)
│   ├── models.py          # DB models
│   ├── views.py           # App + API views
│   ├── services.py        # Business logic
│   ├── forms.py           # Forms
│   ├── urls_*.py          # Route modules
│   ├── templates/         # HTML templates
│   └── static/            # CSS, JS, assets
├── manage.py
└── requirements.txt

👉 Everything important lives in core/ (this is what devs care about)

🚀 Quick Start
git clone https://github.com/yourusername/trendpulse.git
cd trendpulse/django_project

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
CREATE DATABASE trendpulse;
cp .env.example .env
python manage.py migrate
python manage.py seed
python manage.py runserver

👉 http://localhost:8000

Demo: demo@example.com / password123

🔗 Main Routes
/dashboard/ → Dashboard
/api/analyze/ → Analyze topic
/api/history/ → History
/api/saved-ideas/ → Saved ideas
/admin/ → Admin
🛠️ Stack

Django · MySQL · HTML/CSS/JS

📝 License

MIT
