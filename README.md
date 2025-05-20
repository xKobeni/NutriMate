# NutriMate

**NutriMate** is a Machine Learning-Powered Meal Planner web application built with Flask and SQLite. It features user authentication, a modern UI with Tailwind CSS, and a modular, scalable project structure.

## Features
- User registration and login with secure password hashing
- Show/hide password toggle for better UX
- User dashboard (protected route)
- Logout functionality
- Clean, modern UI using Tailwind CSS
- Organized codebase using Flask blueprints

## Project Structure
```
NutriMate/
│
├── app.py                # Main entry point, registers blueprints
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
│
├── models/
│   └── models.py         # Database models and DB functions
│
├── routes/
│   ├── __init__.py       # Makes routes a package
│   ├── auth.py           # Authentication (login, register, logout)
│   └── dashboard.py      # Dashboard and user-protected routes
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   └── dashboard.html
│
├── static/               # For static files (CSS, JS, images)
│
├── instance/
│   └── nutrimate.db      # Your SQLite database
│
└── utils/                # Utility/helper functions (if needed)
```

## Setup Instructions
1. **Clone the repository**
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application**
   ```bash
   python app.py
   ```
4. **Access the app**
   - Open your browser and go to `http://127.0.0.1:5000`

## Usage
- Register a new account at `/register`
- Log in at `/login`
- Access your dashboard at `/dashboard` (must be logged in)
- Log out at `/logout`

## Security Notes
- Passwords are hashed using Werkzeug before being stored in the database.
- Session management is handled securely with Flask's session system.

## Customization
- Update the UI in the `templates/` folder using Tailwind CSS.
- Add new features by creating new blueprints in the `routes/` folder.
- Extend the database models in `models/models.py` as needed.

## License
This project is for educational purposes. Please add your own license if you plan to use it in production. 