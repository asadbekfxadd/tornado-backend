import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql+pg8000://postgres:postgres123@localhost/fitapp")
    SQLALCHEMY_DATABASE_URI = DATABASE_URL.replace("postgresql://", "postgresql+pg8000://") if DATABASE_URL else "postgresql+pg8000://postgres:postgres123@localhost/fitapp"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
