from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.secret_key = 'your-secret-key'

    CORS(app)  # Enable CORS

    from app.routes import chatbot_bp
    app.register_blueprint(chatbot_bp)

    return app
