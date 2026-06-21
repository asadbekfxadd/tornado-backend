from flask import Flask
from extensions import db
from flask_cors import CORS
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    CORS(app)

    from routes.disciplines import disciplines_bp
    from routes.users import users_bp

    app.register_blueprint(disciplines_bp, url_prefix="/api/disciplines")
    app.register_blueprint(users_bp, url_prefix="/api/users")

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
