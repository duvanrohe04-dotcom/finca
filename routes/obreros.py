from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from models import Obrero
from extensions import db
from datetime import datetime

obreros_bp = Blueprint('obreros', __name__)

@obreros_bp.route('/obreros')
@login_required
def index():
    obreros = Obrero.query.all()
    total_nomina = sum(o.total_pago for o in obreros if o.activo)
    return render_template('obreros.html', obreros=obreros, total_nomina=total_nomina)

@obreros_bp.route('/obreros/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo():
    if request.method == 'POST':
        fecha_str = request.form.get('fecha_inicio')
        obrero = Obrero(
            nombre=request.form.get('nombre'),
            cedula=request.form.get('cedula'),
            cargo=request.form.get('cargo'),
            precio_dia=float(request.form.get('precio_dia', 0)),
            dias_trabajados=int(request.form.get('dias_trabajados', 0)),
            fecha_inicio=datetime.strptime(fecha_str, '%Y-%m-%d').date() if fecha_str else None,
            activo=True,
            observaciones=request.form.get('observaciones')
        )
        db.session.add(obrero)
        db.session.commit()
        flash('Obrero registrado exitosamente', 'success')
        return redirect(url_for('obreros.index'))
    return render_template('obreros_form.html', obrero=None)

@obreros_bp.route('/obreros/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    obrero = Obrero.query.get_or_404(id)
    if request.method == 'POST':
        fecha_str = request.form.get('fecha_inicio')
        obrero.nombre = request.form.get('nombre')
        obrero.cedula = request.form.get('cedula')
        obrero.cargo = request.form.get('cargo')
        obrero.precio_dia = float(request.form.get('precio_dia', 0))
        obrero.dias_trabajados = int(request.form.get('dias_trabajados', 0))
        obrero.fecha_inicio = datetime.strptime(fecha_str, '%Y-%m-%d').date() if fecha_str else None
        obrero.activo = 'activo' in request.form
        obrero.observaciones = request.form.get('observaciones')
        db.session.commit()
        flash('Obrero actualizado', 'success')
        return redirect(url_for('obreros.index'))
    return render_template('obreros_form.html', obrero=obrero)

@obreros_bp.route('/obreros/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    obrero = Obrero.query.get_or_404(id)
    db.session.delete(obrero)
    db.session.commit()
    flash('Obrero eliminado', 'success')
    return redirect(url_for('obreros.index'))
