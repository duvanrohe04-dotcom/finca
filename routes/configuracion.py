from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import Usuario
from extensions import db

config_bp = Blueprint('config', __name__)

@config_bp.route('/configuracion', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        accion = request.form.get('accion')

        if accion == 'cambiar_password':
            password_actual = request.form.get('password_actual')
            password_nuevo = request.form.get('password_nuevo')
            password_confirmar = request.form.get('password_confirmar')

            if not check_password_hash(current_user.password, password_actual):
                flash('La contraseña actual es incorrecta', 'error')
            elif password_nuevo != password_confirmar:
                flash('Las contraseñas nuevas no coinciden', 'error')
            elif len(password_nuevo) < 6:
                flash('La contraseña debe tener al menos 6 caracteres', 'error')
            else:
                current_user.password = generate_password_hash(password_nuevo)
                db.session.commit()
                flash('Contraseña actualizada exitosamente', 'success')

        elif accion == 'cambiar_nombre':
            nombre = request.form.get('nombre')
            username = request.form.get('username')
            if nombre and username:
                current_user.nombre = nombre
                existing = Usuario.query.filter_by(username=username).first()
                if existing and existing.id != current_user.id:
                    flash('Ese nombre de usuario ya existe', 'error')
                else:
                    current_user.username = username
                    db.session.commit()
                    flash('Datos actualizados exitosamente', 'success')

    return render_template('configuracion.html')
