from flask import Flask
from werkzeug.security import generate_password_hash
import os
from extensions import db, login_manager

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'finca-secret-key-2024'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finca.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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

    with app.app_context():
        db.create_all()
        seed_admin()

    return app

def seed_admin():
    from models import Usuario
    if not Usuario.query.filter_by(username='admin').first():
        admin = Usuario(
            username='admin',
            password=generate_password_hash('admin123'),
            nombre='Administrador'
        )
        db.session.add(admin)
        db.session.commit()

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
