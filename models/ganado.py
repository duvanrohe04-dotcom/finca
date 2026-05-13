from extensions import db
from datetime import datetime

class Ganado(db.Model):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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
