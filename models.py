from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Espacio(db.Model):
    __tablename__ = 'espacio'

    id = db.Column(db.Integer, primary_key=True)
    ocupado = db.Column(db.Boolean, default=False)
    reservado = db.Column(db.Boolean, default=False)
    disponible = db.Column(db.Boolean, default=True)
    hora_inicio = db.Column(db.DateTime, nullable=True)
    tiempo_transcurrido = db.Column(db.Integer, default=0)
    alerta_enviada = db.Column(db.Boolean, default=False)
    usuario_reserva = db.Column(db.String(100), nullable=True)
    expira_reserva = db.Column(db.DateTime, nullable=True)
    ultima_actualizacion = db.Column(db.DateTime, nullable=True)

    reservas = db.relationship('Reserva', backref='espacio', lazy=True)
    facturas = db.relationship('Factura', backref='espacio', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "ocupado": self.ocupado,
            "reservado": self.reservado,
            "disponible": self.disponible,
            "hora_inicio": self.hora_inicio.strftime('%H:%M:%S') if self.hora_inicio else None,
            "tiempo_transcurrido": self.tiempo_transcurrido,
            "alerta_enviada": self.alerta_enviada,
            "usuario_reserva": self.usuario_reserva,
            "expira_reserva": self.expira_reserva.strftime('%H:%M:%S') if self.expira_reserva else None,
            "ultima_actualizacion": self.ultima_actualizacion.strftime('%H:%M:%S') if self.ultima_actualizacion else None
        }

class Reserva(db.Model):
    __tablename__ = 'reserva'

    id = db.Column(db.Integer, primary_key=True)
    espacio_id = db.Column(db.Integer, db.ForeignKey('espacio.id'), nullable=False)
    usuario = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(50), nullable=False)
    fecha_reserva = db.Column(db.DateTime, default=datetime.now)
    expira = db.Column(db.DateTime, nullable=True)
    estado = db.Column(db.String(20), default='activa')
    origen = db.Column(db.String(20), default='web')

class Factura(db.Model):
    __tablename__ = 'factura'

    id = db.Column(db.Integer, primary_key=True)
    espacio_id = db.Column(db.Integer, db.ForeignKey('espacio.id'), nullable=False)
    fecha_inicio = db.Column(db.DateTime, nullable=False)
    fecha_fin = db.Column(db.DateTime, nullable=False)
    tiempo_minutos = db.Column(db.Integer, nullable=False)
    monto = db.Column(db.Float, nullable=False)
    estado = db.Column(db.String(20), default='completado')

class UsuarioTelegram(db.Model):
    __tablename__ = 'usuario_telegram'

    id = db.Column(db.Integer, primary_key=True)
    telefono = db.Column(db.String(50), unique=True, nullable=False)
    chat_id = db.Column(db.String(50), unique=True, nullable=False)