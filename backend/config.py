import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    # Flask
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "dev-jwt-secret-key")

    ENV = os.environ.get("FLASK_ENV", "development")
    DEBUG = True

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "mysql+pymysql://studenthub:studenthubpw@127.0.0.1:3306/studenthub_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Uploads
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

    # Mail
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.hostinger.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "info@nuhvin.com")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "NGS@email26")

    # Dev options
    DEV_SQLITE_FALLBACK = True
    AUTO_CREATE_DB = True
