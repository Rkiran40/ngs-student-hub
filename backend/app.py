import os
import sys
from dotenv import load_dotenv  # <-- load .env
load_dotenv()  # Load environment variables from .env

# Ensure proper package resolution when running as __main__
if __name__ == '__main__' and __package__ is None:
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, repo_root)
    __package__ = 'backend'

from flask import Flask, jsonify
from flask_cors import CORS
from backend.config import Config
from backend.db import db
from backend.auth import jwt
from backend.logging_config import setup_logging

# configure logging as early as possible
setup_logging()


def create_app(config_overrides: dict | None = None):
    app = Flask(__name__, static_folder=None)

    # Load config from Config class
    app.config.from_object(Config)

    # Override config from environment variables (loaded by dotenv)
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", app.config['SECRET_KEY'])
    app.config['JWT_SECRET_KEY'] = os.environ.get("JWT_SECRET_KEY", app.config['JWT_SECRET_KEY'])
    app.config['MAIL_USERNAME'] = os.environ.get("MAIL_USERNAME", app.config.get('MAIL_USERNAME'))
    app.config['MAIL_PASSWORD'] = os.environ.get("MAIL_PASSWORD", app.config.get('MAIL_PASSWORD'))

    # Apply runtime config overrides
    if config_overrides:
        app.config.update(config_overrides)

    # Configure CORS
    cors_origins = app.config.get('CORS_ORIGINS', '*')
    CORS(
        app,
        supports_credentials=True,
        resources={r"/*": {"origins": cors_origins}},
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )

    # Test DB connection early
    from sqlalchemy import create_engine, text
    db_uri = app.config.get('SQLALCHEMY_DATABASE_URI')
    print('DB URI at init:', db_uri)
    fallback_used = False
    try:
        engine = create_engine(db_uri)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            print("✅ Database connection successful")
    except Exception as e:
        fallback_allowed = app.config.get('DEV_SQLITE_FALLBACK', False) and app.config.get('ENV', 'production') != 'production'
        if fallback_allowed and not app.config.get('TESTING', False):
            fallback_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dev_fallback.db')
            fallback_uri = f"sqlite:///{fallback_path}"
            print(f"⚠ WARNING: failed to connect to DB ({e}); falling back to SQLite at {fallback_uri}")
            app.config['SQLALCHEMY_DATABASE_URI'] = fallback_uri
            fallback_used = True
        else:
            print('❌ ERROR: failed to connect to DB (no fallback allowed):', e)
            raise

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        # Import models so SQLAlchemy knows them
        try:
            print('IMPORTING backend.models')
            from . import models  # noqa: F401
            print('IMPORTED backend.models')
            app.logger.info('Imported backend.models')
        except Exception as e:
            print('FAILED to import backend.models', e)
            app.logger.exception('Failed to import backend.models')

        # SQLite fallback: create tables if needed
        if fallback_used and not app.config.get('TESTING', False):
            try:
                print('Fallback to SQLite detected — creating tables with db.create_all()')
                db.create_all()
            except Exception as e:
                print('Failed to create tables on fallback SQLite:', e)

        # Seed dev admin (always ensure admin@nuhvin.com exists)
        if os.environ.get('DEV_AUTO_SEED', '1').lower() in ('1', 'true', 'yes'):
            try:
                from backend.models import User, Profile
                from backend.utils import hash_password

                admin_email = os.environ.get('DEV_ADMIN_EMAIL', 'admin@nuhvin.com')
                admin_username = os.environ.get('DEV_ADMIN_USERNAME', admin_email)
                admin_password = os.environ.get('DEV_ADMIN_PASSWORD', 'Admin@123')

                existing = User.query.filter_by(email=admin_email).first()
                if existing:
                    print('Dev admin exists:', admin_email)
                    if existing.role != 'admin':
                        existing.role = 'admin'
                    if existing.profile:
                        existing.profile.username = admin_username
                        existing.profile.status = 'active'
                    else:
                        p = Profile(
                            user_id=existing.id,
                            username=admin_username,
                            full_name=admin_username,
                            email=admin_email,
                            status='active'
                        )
                        db.session.add(p)
                    db.session.commit()
                else:
                    u = User(
                        email=admin_email,
                        password_hash=hash_password(admin_password),
                        role='admin'
                    )
                    db.session.add(u)
                    db.session.commit()
                    p = Profile(
                        user_id=u.id,
                        username=admin_username,
                        full_name=admin_username,
                        email=admin_email,
                        status='active'
                    )
                    db.session.add(p)
                    db.session.commit()
                    print('Created dev admin', admin_email)
            except Exception as e:
                print('Failed to seed dev admin:', e)

        # Optional automatic table creation
        if os.environ.get('AUTO_CREATE_DB', '0').lower() in ('1', 'true', 'yes') and not app.config.get('TESTING', False):
            if app.config.get('ENV') == 'production':
                app.logger.warning('AUTO_CREATE_DB is enabled in production; skipping automatic create_all() for safety.')
            else:
                db.create_all()

    # Register blueprints
    from .routes.auth import auth_bp
    from .routes.student import student_bp
    from .routes.admin import admin_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(student_bp, url_prefix="/student")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    # Serve uploaded files
    @app.route('/uploads/<path:relpath>')
    def serve_upload(relpath):
        from flask import send_from_directory
        uploads_root = app.config.get('UPLOAD_FOLDER')
        rel_parts = [p for p in relpath.replace('\\', '/').split('/') if p and p != '..']
        full = os.path.join(uploads_root, *rel_parts)
        if not os.path.isfile(full):
            return jsonify({'success': False, 'message': 'File not found'}), 404
        return send_from_directory(uploads_root, '/'.join(rel_parts))

    # Health endpoints
    @app.get('/')
    def health():
        return jsonify({"status": "ok"})

    @app.get('/healthz')
    def healthz():
        return jsonify({"status": "ok"})

    @app.get('/live')
    def live():
        return jsonify({"status": "ok"})

    @app.get('/ready')
    def ready():
        try:
            with db.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return jsonify({"status": "ok"})
        except Exception:
            app.logger.exception('Readiness check failed')
            return jsonify({"status": "error", "message": "db unavailable"}), 500

    # Prometheus metrics
    try:
        from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
        from flask import Response

        @app.get('/metrics')
        def metrics():
            try:
                data = generate_latest()
                return Response(data, mimetype=CONTENT_TYPE_LATEST)
            except Exception:
                return jsonify({'status': 'error', 'message': 'metrics unavailable'}), 500
    except Exception:
        app.logger.info('prometheus_client not available; /metrics disabled')

    # Sentry initialization
    sentry_dsn = os.environ.get('SENTRY_DSN') or app.config.get('SENTRY_DSN')
    if sentry_dsn:
        try:
            import sentry_sdk
            from sentry_sdk.integrations.flask import FlaskIntegration
            sentry_sdk.init(dsn=sentry_dsn, integrations=[FlaskIntegration()],
                            traces_sample_rate=float(os.environ.get('SENTRY_TRACES_SAMPLE_RATE', '0.0')))
            app.logger.info('Sentry initialized')
        except Exception:
            app.logger.exception('Failed to initialize Sentry')

    return app



app = create_app()
# RAILWAY-SAFE RUN
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    create_app().run(host='0.0.0.0', port=port, debug=False)
