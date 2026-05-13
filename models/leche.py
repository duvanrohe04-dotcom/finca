from extensions import db
from datetime import datetime

class RegistroLeche(db.Model):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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
