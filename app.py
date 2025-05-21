from flask import Flask, render_template
from models.models import init_db
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.profile import profile_bp
from routes.preferences import preferences_bp

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Needed for session management

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(preferences_bp)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    init_db()  # Initialize database before running the app
    app.run(debug=True)