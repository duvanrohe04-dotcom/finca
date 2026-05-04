from extensions import db
from flask_login import UserMixin
from datetime import datetime

class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)

class Ganado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    numero = db.Column(db.String(50))
    raza = db.Column(db.String(100))
    fecha_nacimiento = db.Column(db.Date)
    madre_id = db.Column(db.Integer, db.ForeignKey('ganado.id'), nullable=True)
    padre_id = db.Column(db.Integer, db.ForeignKey('ganado.id'), nullable=True)
    tipo = db.Column(db.String(20), default='adulto')  # adulto, ternero
    sexo = db.Column(db.String(10))  # macho, hembra
    observaciones = db.Column(db.Text)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

    madre = db.relationship('Ganado', foreign_keys=[madre_id], remote_side='Ganado.id', backref='terneros_madre')
    padre = db.relationship('Ganado', foreign_keys=[padre_id], remote_side='Ganado.id', backref='terneros_padre')

class Obrero(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    cedula = db.Column(db.String(20))
    cargo = db.Column(db.String(100))
    precio_dia = db.Column(db.Float, default=0)
    dias_trabajados = db.Column(db.Integer, default=0)
    fecha_inicio = db.Column(db.Date)
    activo = db.Column(db.Boolean, default=True)
    observaciones = db.Column(db.Text)

    @property
    def total_pago(self):
        return self.precio_dia * self.dias_trabajados

class BultoInventario(db.Model):
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

class RegistroLeche(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    litros_manana = db.Column(db.Float, default=0)
    litros_tarde = db.Column(db.Float, default=0)
    precio_litro = db.Column(db.Float, default=0)
    observaciones = db.Column(db.Text)

    @property
    def total_litros(self):
        return self.litros_manana + self.litros_tarde

    @property
    def total_dinero(self):
        return self.total_litros * self.precio_litro
