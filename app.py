from flask import Flask, send_from_directory, make_response
from werkzeug.security import generate_password_hash
import os

# Carga automática del archivo .env (si python-dotenv está instalado)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from extensions import db, login_manager
from conf.settings import get_config

def create_app():
    app = Flask(__name__)

    # ── Configuración desde conf/settings.py (lee el .env) ──
    app.config.from_object(get_config())

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Debes iniciar sesión para acceder.'

    from routes.auth import auth_bp
    from routes.ganado import ganado_bp
    from routes.obreros import obreros_bp
    from routes.inventario import inventario_bp
    from routes.leche import leche_bp
    from routes.configuracion import config_bp
    from routes.dashboard import dashboard_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(ganado_bp)
    app.register_blueprint(obreros_bp)
    app.register_blueprint(inventario_bp)
    app.register_blueprint(leche_bp)
    app.register_blueprint(config_bp)
    app.register_blueprint(dashboard_bp)

    @app.route('/favicon.ico')
    def favicon():
        resp = make_response(
            send_from_directory(app.static_folder, 'favicon.ico', mimetype='image/vnd.microsoft.icon')
        )
        resp.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        resp.headers['Pragma'] = 'no-cache'
        resp.headers['Expires'] = '0'
        return resp

    with app.app_context():
        db.create_all()
        seed_admin()

    return app

def seed_admin():
    try:
        from models import Usuario
        if not Usuario.query.filter_by(username='admin').first():
            admin = Usuario(  # type: ignore[call-arg]
                username='admin',
                password=generate_password_hash('admin123'),
                nombre='Administrador'
            )
            db.session.add(admin)
            db.session.commit()
    except Exception as e:
        print(f'[seed_admin] Advertencia: {e}')

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
