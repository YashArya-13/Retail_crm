# Retail CRM

A simple, responsive CRM prototype inspired by Zoho CRM. Built with Python, Flask, and SQLite, featuring basic lead/task tracking and Google OAuth login.

## Features

- **Dashboard**: Quick overview of active leads, won deals, revenue pipeline, and pending tasks.
- **Lead Management**: Form to add new leads dynamically on the dashboard.
- **Task List**: Interactive check-off list for daily items.
- **Profile Page**: Form to update user details (name, address, education) and upload a profile photo.
- **Authentication**: Email/password registration and Google OAuth support.

## Tech Stack

- **Backend**: Flask, Flask-SQLAlchemy, Flask-Login, Flask-Dance (Google OAuth)
- **Frontend**: Bootstrap 5, Bootstrap Icons, Custom CSS/JS
- **Database**: SQLite

## Setup & Installation

1. **Clone the repository and install requirements:**
   ```bash
   git clone https://github.com/YashArya-13/Retail_crm.git
   cd Retail_crm
   
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   
   pip install -r requirements.txt
   ```

2. **Set up the environment:**
   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=some-random-secret-key
   GOOGLE_CLIENT_ID=your-google-client-id
   GOOGLE_CLIENT_SECRET=your-google-client-secret
   OAUTHLIB_INSECURE_TRANSPORT=1
   ```
   *Note: If you plan to use Google Sign-in, make sure to configure and download your `client_secret.json` from the Google Developer Console and place it in the project root.*

3. **Run the local server:**
   ```bash
   python app.py
   ```
   Access the app at `http://127.0.0.1:5000` in your web browser.

## Project Structure

- `app.py`: Routing, page actions, and OAuth handler.
- `models.py`: Database models (User and Profile schemas).
- `config.py`: Core configurations (SQLite URI and tracking).
- `templates/`: HTML templates (login, signup, base, dashboard, profile).
- `static/`: Custom stylesheets and user uploads.
