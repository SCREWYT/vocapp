from flask import Flask

def create_app():
    app = Flask(__name__)

    # Konfiguration
    app.config.from_mapping(
        SECRET_KEY='dev',  # für Sessions, CSRF etc.
        DATABASE='sqlite.db'  # Pfad zur SQLite-Datei
    )

    # Importiere und registriere Blueprints hier
    # from . import auth
    # app.register_blueprint(auth.bp)

    # Datenbankverbindung vorbereiten
    # from . import db
    # db.init_app(app)

    @app.route('/')
    def index():
        return 'Hallo, VocApp!'

    return app
