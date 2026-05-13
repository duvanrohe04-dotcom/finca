from extensions import db

class Obrero(db.Model):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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
