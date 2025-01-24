from dotenv import load_dotenv
from flask import Flask
from markupsafe import Markup
from flask_cors import CORS

from app.common.pre_check import check_env_vars

load_dotenv()
Markup()
Markup('')

def create_app():
    
    app = Flask(__name__)
    cors = CORS(app)

    # Note: Every module in this app assumes the app context is available and initialized.
    with app.app_context():
        check_env_vars()

        from app.routes.health import bp as health_bp

        app.register_blueprint(health_bp)
        return app
