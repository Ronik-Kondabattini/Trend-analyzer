# Contributing to Trend Analyzer

Thank you for considering contributing to Trend Analyzer! Your contributions make this project better for everyone.

## Development Setup

The backend is built with Django. Follow these steps to set up your development environment.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Ronik-Kondabattini/Trend-analyzer.git
   cd Trend-analyzer/backend
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows: venv\Scripts\activate
   # On macOS/Linux: source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Copy `.env.example` to `.env` if available, and configure your database settings.
   Ensure `.env` is never committed to version control.

5. **Run Migrations & Start Server:**
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

## Pull Request Process

1. Fork the repository.
2. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes and test them locally.
4. Commit your changes with clear, descriptive messages:
   ```bash
   git commit -m "Add feature: your feature name"
   ```
5. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
6. Open a Pull Request against the `main` branch. Provide a clear description of your changes.

## Code Style
- Follow [PEP 8](https://peps.python.org/pep-0008/) for Python code.
- Write docstrings for all major functions and classes.
- Ensure your changes do not break existing tests.
