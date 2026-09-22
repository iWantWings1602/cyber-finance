# CyberFinance - Personal Finance Tracker

A Django application for tracking personal finance, income, and expenses by categories with flexible transaction tagging. This project was developed as part of a Python course assignment.

##  Model Architecture
- **Account** — User financial accounts (Cash, Cards, Crypto) with choices-based types and calculated custom property validation.
- **Category** — Financial operation categories (Expenses / Income).
- **Tag** — Analytical tags for custom financial tracking (connected via ManyToManyField to Transactions).
- **Transaction** — The core model tracking money movements (connected via ForeignKey to Account and Category).

##  Technical Features
- Built with Django ORM for complex data filtration and aggregation logic.
- Fully customized professional Admin Dashboard featuring advanced list displays, filters, search utilities, and custom Admin Actions.
- Includes a standalone `queries.py` database test script showcasing native ORM queries and their RAW SQL representations.
- Production-ready configuration: environment variables (.env), WhiteNoise static file serving, and Gunicorn integration.

##  How to Run Locally

1. Clone the repository and navigate to the project root:
   ```bash
   git clone https://github.com
   cd cyber-finance
   ```

2. Create and activate a Python virtual environment:
   ```bash
   python -m venv .venv
   # For Windows:
   .venv\Scripts\activate
   # For Mac/Linux:
   source .venv/bin/activate
   ```

3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   * Create a `.env` file in the root directory (next to `manage.py`).
   * Copy the template from `.env.example` and fill in your actual values:
     ```text
     SECRET_KEY=your-secret-key-here
     DEBUG=True
     ALLOWED_HOSTS=127.0.0.1,localhost
     ```

5. Run database migrations:
   ```bash
   python manage.py migrate
   ```

6. Create an administrative user for dashboard access:
   ```bash
   python manage.py createsuperuser
   ```

7. Start the local development server:
   ```bash
   python manage.py runserver
   ```

##  Live Demo
*(Will be added after the deployment lesson on Render.com)*

## 📊 Admin Dashboard Screenshot
![Django Admin Dashboard](screenshot.png)
