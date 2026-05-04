from flask import Blueprint, render_template
from extensions import db
from flask_login import login_required
from models import Ganado, Obrero, BultoInventario, DrugaInventario, RegistroLeche
from datetime import datetime, date

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def index():
    total_ganado = Ganado.query.filter_by(tipo='adulto').count()
    total_terneros = Ganado.query.filter_by(tipo='ternero').count()
    total_obreros = Obrero.query.filter_by(activo=True).count()

    bultos = BultoInventario.query.all()
    drogas = DrugaInventario.query.all()
    total_inv_bultos = sum(b.total for b in bultos)
    total_inv_drogas = sum(d.total for d in drogas)

    hoy = date.today()
    mes = hoy.month
    anio = hoy.year
    registros_leche = RegistroLeche.query.filter(
        RegistroLeche.fecha >= date(anio, mes, 1)
    ).all()
    total_litros_mes = sum(r.total_litros for r in registros_leche)

    return render_template('dashboard.html',
        total_ganado=total_ganado,
        total_terneros=total_terneros,
        total_obreros=total_obreros,
        total_inv_bultos=total_inv_bultos,
        total_inv_drogas=total_inv_drogas,
        total_litros_mes=total_litros_mes,
        fecha_hoy=hoy.strftime('%d/%m/%Y')
    )
