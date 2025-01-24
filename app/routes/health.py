from flask import Blueprint, current_app

bp = Blueprint("health", __name__)

@bp.route("/health", methods=["GET"])
def health_check():
    current_app.logger.info("Health check !!!")
    return {"status": "ok"}, 200
    