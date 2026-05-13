from extensions import db
from datetime import datetime

class BultoInventario(db.Model):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    marca = db.Column(db.String(100))
    precio_unitario = db.Column(db.Float, default=0)
    cantidad = db.Column(db.Integer, default=0)
    unidad = db.Column(db.String(30), default='bulto')
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def total(self):
        return self.precio_unitario * self.cantidad

class DrugaInventario(db.Model):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    marca = db.Column(db.String(100))
    precio_unitario = db.Column(db.Float, default=0)
    cantidad = db.Column(db.Integer, default=0)
    unidad = db.Column(db.String(30), default='unidad')
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def total(self):
        return self.precio_unitario * self.cantidad
