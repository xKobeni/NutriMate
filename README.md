# NutriMate

**NutriMate** is a Machine Learning-Powered Meal Planner web application built with Flask and SQLite. It features user authentication, personalized meal planning, and a modern UI with Bootstrap CSS.

## Features
- User registration and login with secure password hashing
- User profile management with detailed health information
- Dietary preferences system with validation
- Calorie and macronutrient calculations
- Personalized dashboard with health metrics
- Clean, modern UI using Bootstrap CSS
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
│   ├── models.py         # Database models and DB functions
│   └── calorie_model.py  # Calorie calculation logic
│
├── routes/
│   ├── __init__.py       # Makes routes a package
│   ├── auth.py           # Authentication (login, register, logout)
│   ├── profile.py        # User profile management
│   ├── preferences.py    # Dietary preferences management
│   └── dashboard.py      # Dashboard and user-protected routes
│
├── templates/
│   ├── base.html         # Base template with common elements
│   ├── index.html        # Landing page
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   ├── profile.html      # Profile management page
│   ├── preferences.html  # Dietary preferences page
│   └── dashboard.html    # User dashboard
│
├── static/               # Static files
│   ├── css/             # Stylesheets
│   └── js/              # JavaScript files
│
├── instance/
│   └── nutrimate.db      # SQLite database
│
└── docs/                 # Documentation
    ├── flow.txt          # System flow documentation
    └── projectContext.txt # Project context and requirements
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
- Complete your profile at `/profile`
- Set dietary preferences at `/preferences`
- Access your dashboard at `/dashboard` (must be logged in)
- Log out at `/logout`

## Features in Detail

### User Profile System
- Collects essential health information
- Validates user inputs
- Stores profile data securely
- Allows profile updates

### Dietary Preferences
- Diet type selection (regular, vegetarian, vegan, keto, etc.)
- Allergy management
- Health goal setting
- Optional calorie limit
- Comprehensive input validation

### Calorie Calculations
- Basal Metabolic Rate (BMR) calculation
- Total Daily Energy Expenditure (TDEE)
- Calorie goals for different objectives
- Macronutrient distribution recommendations

### Dashboard
- Profile summary
- Dietary preferences overview
- Daily energy needs
- Calorie goals
- Macronutrient recommendations

## Security Notes
- Passwords are hashed using Werkzeug
- Session management is handled securely
- Input validation on all forms
- Protected routes with login requirements

## Upcoming Features
- Machine learning-based meal recommendations
- Meal planning system
- Meal logging and tracking
- Progress monitoring
- Feedback system for recommendations

## License
This project is for educational purposes. Please add your own license if you plan to use it in production. 