from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from models import Ganado
from extensions import db
from datetime import datetime

ganado_bp = Blueprint('ganado', __name__)

@ganado_bp.route('/ganado')
@login_required
def index():
    adultos = Ganado.query.filter_by(tipo='adulto').all()
    terneros = Ganado.query.filter_by(tipo='ternero').all()
    return render_template('ganado.html', adultos=adultos, terneros=terneros)

@ganado_bp.route('/ganado/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo():
    todos = Ganado.query.all()
    if request.method == 'POST':
        fecha_str = request.form.get('fecha_nacimiento')
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date() if fecha_str else None
        animal = Ganado(
            nombre=request.form.get('nombre'),
            numero=request.form.get('numero'),
            raza=request.form.get('raza'),
            fecha_nacimiento=fecha,
            madre_id=request.form.get('madre_id') or None,
            padre_id=request.form.get('padre_id') or None,
            tipo=request.form.get('tipo', 'adulto'),
            sexo=request.form.get('sexo'),
            observaciones=request.form.get('observaciones')
        )
        db.session.add(animal)
        db.session.commit()
        flash('Animal registrado exitosamente', 'success')
        return redirect(url_for('ganado.index'))
    return render_template('ganado_form.html', animal=None, todos=todos)

@ganado_bp.route('/ganado/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    animal = Ganado.query.get_or_404(id)
    todos = Ganado.query.filter(Ganado.id != id).all()
    if request.method == 'POST':
        fecha_str = request.form.get('fecha_nacimiento')
        animal.nombre = request.form.get('nombre')
        animal.numero = request.form.get('numero')
        animal.raza = request.form.get('raza')
        animal.fecha_nacimiento = datetime.strptime(fecha_str, '%Y-%m-%d').date() if fecha_str else None
        animal.madre_id = request.form.get('madre_id') or None
        animal.padre_id = request.form.get('padre_id') or None
        animal.tipo = request.form.get('tipo', 'adulto')
        animal.sexo = request.form.get('sexo')
        animal.observaciones = request.form.get('observaciones')
        db.session.commit()
        flash('Animal actualizado', 'success')
        return redirect(url_for('ganado.index'))
    return render_template('ganado_form.html', animal=animal, todos=todos)

@ganado_bp.route('/ganado/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    animal = Ganado.query.get_or_404(id)
    db.session.delete(animal)
    db.session.commit()
    flash('Animal eliminado', 'success')
    return redirect(url_for('ganado.index'))
