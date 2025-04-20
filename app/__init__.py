from dotenv import load_dotenv
from flask import Flask, g, current_app
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

        # from app.routes.health import bp as health_bp
        # from app.routes.search import sr as search_bp

        from app import routes
        from app import views
        from app.services import ad

        app.register_blueprint(routes.bp)
        app.register_blueprint(routes.sr)
        app.register_blueprint(ad)
        
        current_app.route('/')

        g.DEFAULT_MODEL = "llama-3.2:latest"
        g.DEFAULT_URL = "http://localhost:11434"
        g.DEFAULT_TEMPERATURE = 0.0
        g.DEFAULT_MAX_TOKENS = 0

        return app
