from flask import Flask, render_template
from flask_login import LoginManager, UserMixin

from app.config import Config
from app.routes.public import public_bp


login_manager = LoginManager()
login_manager.login_view = "admin.login"


class AdminUser(UserMixin):
    """Minimal user model for Flask-Login setup stage."""

    def __init__(self, user_id: str) -> None:
        self.id = user_id


@login_manager.user_loader
def load_user(user_id: str) -> AdminUser:
    # Placeholder loader for setup phase.
    return AdminUser(user_id=user_id)


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    from app.routes.admin import admin_bp

    login_manager.init_app(app)
    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template("errors/500.html"), 500

    return app
