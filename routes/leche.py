from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from models import RegistroLeche
from extensions import db
from datetime import datetime, date

leche_bp = Blueprint('leche', __name__)

@leche_bp.route('/leche')
@login_required
def index():
    registros = RegistroLeche.query.order_by(RegistroLeche.fecha.desc()).all()
    total_litros = sum(r.total_litros for r in registros)
    total_dinero = sum(r.total_dinero for r in registros)
    return render_template('leche.html',
        registros=registros,
        total_litros=total_litros,
        total_dinero=total_dinero)

@leche_bp.route('/leche/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo():
    if request.method == 'POST':
        fecha_str = request.form.get('fecha')
        registro = RegistroLeche(
            fecha=datetime.strptime(fecha_str, '%Y-%m-%d').date() if fecha_str else date.today(),
            litros_manana=float(request.form.get('litros_manana', 0)),
            litros_tarde=float(request.form.get('litros_tarde', 0)),
            precio_litro=float(request.form.get('precio_litro', 0)),
            observaciones=request.form.get('observaciones')
        )
        db.session.add(registro)
        db.session.commit()
        flash('Registro de leche guardado', 'success')
        return redirect(url_for('leche.index'))
    return render_template('leche_form.html', registro=None, hoy=date.today().strftime('%Y-%m-%d'))

@leche_bp.route('/leche/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    registro = RegistroLeche.query.get_or_404(id)
    if request.method == 'POST':
        fecha_str = request.form.get('fecha')
        registro.fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date() if fecha_str else date.today()
        registro.litros_manana = float(request.form.get('litros_manana', 0))
        registro.litros_tarde = float(request.form.get('litros_tarde', 0))
        registro.precio_litro = float(request.form.get('precio_litro', 0))
        registro.observaciones = request.form.get('observaciones')
        db.session.commit()
        flash('Registro actualizado', 'success')
        return redirect(url_for('leche.index'))
    return render_template('leche_form.html', registro=registro, hoy=registro.fecha.strftime('%Y-%m-%d'))

@leche_bp.route('/leche/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    registro = RegistroLeche.query.get_or_404(id)
    db.session.delete(registro)
    db.session.commit()
    flash('Registro eliminado', 'success')
    return redirect(url_for('leche.index'))
