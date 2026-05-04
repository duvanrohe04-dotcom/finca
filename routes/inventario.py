from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from models import BultoInventario, DrugaInventario
from extensions import db

inventario_bp = Blueprint('inventario', __name__)

@inventario_bp.route('/inventario')
@login_required
def index():
    bultos = BultoInventario.query.all()
    drogas = DrugaInventario.query.all()
    total_bultos = sum(b.total for b in bultos)
    total_drogas = sum(d.total for d in drogas)
    return render_template('inventario.html',
        bultos=bultos, drogas=drogas,
        total_bultos=total_bultos, total_drogas=total_drogas)

# --- BULTOS ---
@inventario_bp.route('/inventario/bulto/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_bulto():
    if request.method == 'POST':
        item = BultoInventario(
            nombre=request.form.get('nombre'),
            marca=request.form.get('marca'),
            precio_unitario=float(request.form.get('precio_unitario', 0)),
            cantidad=int(request.form.get('cantidad', 0)),
            unidad=request.form.get('unidad', 'bulto')
        )
        db.session.add(item)
        db.session.commit()
        flash('Bulto agregado al inventario', 'success')
        return redirect(url_for('inventario.index'))
    return render_template('inventario_bulto_form.html', item=None)

@inventario_bp.route('/inventario/bulto/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_bulto(id):
    item = BultoInventario.query.get_or_404(id)
    if request.method == 'POST':
        item.nombre = request.form.get('nombre')
        item.marca = request.form.get('marca')
        item.precio_unitario = float(request.form.get('precio_unitario', 0))
        item.cantidad = int(request.form.get('cantidad', 0))
        item.unidad = request.form.get('unidad', 'bulto')
        db.session.commit()
        flash('Bulto actualizado', 'success')
        return redirect(url_for('inventario.index'))
    return render_template('inventario_bulto_form.html', item=item)

@inventario_bp.route('/inventario/bulto/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_bulto(id):
    item = BultoInventario.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Bulto eliminado', 'success')
    return redirect(url_for('inventario.index'))

# --- DROGAS ---
@inventario_bp.route('/inventario/droga/nueva', methods=['GET', 'POST'])
@login_required
def nueva_droga():
    if request.method == 'POST':
        item = DrugaInventario(
            nombre=request.form.get('nombre'),
            marca=request.form.get('marca'),
            precio_unitario=float(request.form.get('precio_unitario', 0)),
            cantidad=int(request.form.get('cantidad', 0)),
            unidad=request.form.get('unidad', 'unidad')
        )
        db.session.add(item)
        db.session.commit()
        flash('Medicamento agregado al inventario', 'success')
        return redirect(url_for('inventario.index'))
    return render_template('inventario_droga_form.html', item=None)

@inventario_bp.route('/inventario/droga/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_droga(id):
    item = DrugaInventario.query.get_or_404(id)
    if request.method == 'POST':
        item.nombre = request.form.get('nombre')
        item.marca = request.form.get('marca')
        item.precio_unitario = float(request.form.get('precio_unitario', 0))
        item.cantidad = int(request.form.get('cantidad', 0))
        item.unidad = request.form.get('unidad', 'unidad')
        db.session.commit()
        flash('Medicamento actualizado', 'success')
        return redirect(url_for('inventario.index'))
    return render_template('inventario_droga_form.html', item=item)

@inventario_bp.route('/inventario/droga/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_droga(id):
    item = DrugaInventario.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Medicamento eliminado', 'success')
    return redirect(url_for('inventario.index'))
