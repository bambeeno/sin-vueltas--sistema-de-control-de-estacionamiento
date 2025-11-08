from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import threading
import time
import requests
from conexion import abrir_serial
from models import db, Espacio, Reserva, Factura, UsuarioTelegram

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estacionamiento.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

TELEGRAM_TOKEN = '8211484348:AAGTQx1ZpqaOg11EwbRSR6v_qt5fT-DdLpY'

def enviar_telegram_a(chat_id, mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": mensaje
    }
    try:
        response = requests.post(url, json=payload)
        print(f"📨 Telegram status: {response.status_code}")
        print(response.text)
    except Exception as e:
        print("❌ Error al enviar mensaje:", e)

@app.route('/api/reservar', methods=['POST'])
def reservar():
    data = request.get_json()
    espacio_id = data.get("espacio_id")
    nombre = data.get("nombre")
    telefono = data.get("telefono")

    espacio = Espacio.query.get(espacio_id)
    if not espacio or espacio.ocupado:
        return jsonify({"error": "Espacio no disponible"}), 400

    espacio.ocupado = True
    espacio.disponible = False
    espacio.usuario_reserva = telefono
    espacio.hora_inicio = datetime.now()
    db.session.commit()

    usuario = UsuarioTelegram.query.filter_by(telefono=telefono).first()
    if usuario:
        mensaje = f"✅ Tu reserva fue registrada.\n🚗 Espacio #{espacio_id} reservado a nombre de {nombre}."
        enviar_telegram_a(usuario.chat_id, mensaje)

    return jsonify({"mensaje": "Reserva registrada"}), 200

@app.route('/api/registrar_chat', methods=['POST'])
def registrar_chat():
    data = request.json
    telefono = data.get("telefono")
    chat_id = data.get("chat_id")

    if not telefono or not chat_id:
        return jsonify({"error": "Faltan datos"}), 400

    existente = UsuarioTelegram.query.filter_by(telefono=telefono).first()
    if existente:
        existente.chat_id = chat_id
    else:
        nuevo = UsuarioTelegram(telefono=telefono, chat_id=chat_id)
        db.session.add(nuevo)

    db.session.commit()
    return jsonify({"mensaje": "Chat registrado correctamente"})

@app.route('/api/espacios', methods=['GET'])
def obtener_espacios():
    espacios = Espacio.query.all()
    return jsonify({
        "espacios": [e.to_dict() for e in espacios]
    })

@app.route('/api/liberar/<int:espacio_id>', methods=['POST'])
def liberar_espacio(espacio_id):
    espacio = db.session.get(Espacio, espacio_id)
    if not espacio or not espacio.ocupado:
        return jsonify({"error": "Espacio no ocupado"}), 400

    ahora = datetime.now()
    if not espacio.hora_inicio:
        return jsonify({"error": "No hay hora de inicio registrada"}), 400

    tiempo_total = int((ahora - espacio.hora_inicio).total_seconds() / 60)
    monto = 0
    if tiempo_total > TIEMPO_GRATIS_MINUTOS:
        horas_extra = (tiempo_total - TIEMPO_GRATIS_MINUTOS) // 60
        monto = horas_extra * PRECIO_POR_HORA

    factura = Factura(
        espacio_id=espacio_id,
        fecha_inicio=espacio.hora_inicio,
        fecha_fin=ahora,
        tiempo_minutos=tiempo_total,
        monto=monto,
        estado="completado"
    )
    db.session.add(factura)

    espacio.ocupado = False
    espacio.disponible = True
    espacio.reservado = False
    espacio.hora_inicio = None
    espacio.tiempo_transcurrido = 0
    espacio.alerta_enviada = False
    espacio.ultima_actualizacion = ahora
    db.session.commit()

    if arduino:
        arduino.write(f"L{espacio_id}\n".encode())

    return jsonify({"mensaje": f"Espacio {espacio_id} liberado", "monto": monto})

@app.route('/')
def index():
    return render_template('index.html')

def enviar_alerta_personalizada(chat_id, espacio_id, minutos):
    mensaje = f"""🚗 Tu reserva en el espacio #{espacio_id} está por terminar.

⏰ Han pasado {minutos} minutos.
⏳ Quedan 10 minutos de tiempo gratuito.

Liberá el espacio si ya no lo necesitás."""
    enviar_telegram_a(chat_id, mensaje)

def leer_desde_arduino():
    if arduino:
        try:
            while arduino.in_waiting:
                linea = arduino.readline().decode(errors='ignore').strip()
                print(f"📨 Arduino dice: {linea}")
                if linea.startswith("DATA:"):
                    procesar_linea_data(linea)
        except Exception as e:
            print(f"⚠️ Error leyendo desde Arduino: {e}")

def procesar_linea_data(linea):
    try:
        datos = linea.replace("DATA:", "").split(",")
        for dato in datos:
            if dato.startswith("E"):
                espacio_id, estado = dato[1:].split(":")
                espacio_id = int(espacio_id)
                ocupado = estado == "1"
                espacio = db.session.get(Espacio, espacio_id)
                if espacio:
                    ahora = datetime.now()
                    espacio.ocupado = ocupado
                    espacio.disponible = not ocupado
                    if ocupado and not espacio.hora_inicio:
                        espacio.hora_inicio = ahora
                    elif not ocupado:
                        espacio.hora_inicio = None
                        espacio.tiempo_transcurrido = 0
                        espacio.alerta_enviada = False
                    espacio.ultima_actualizacion = ahora
        db.session.commit()
    except Exception as e:
        print(f"⚠️ Error procesando DATA: {linea} → {e}")

def verificar_tiempos_ocupacion():
    print("🧵 Hilo de verificación iniciado")
    while True:
        with app.app_context():
            leer_desde_arduino()
            ahora = datetime.now()
            espacios = Espacio.query.all()

            for e in espacios:
                e.disponible = not e.ocupado
                if e.ocupado:
                    if e.hora_inicio:
                        minutos = int((ahora - e.hora_inicio).total_seconds() / 60)
                        e.tiempo_transcurrido = minutos
                        if minutos == TIEMPO_GRATIS_MINUTOS - 10 and not e.alerta_enviada:
                            usuario = UsuarioTelegram.query.filter_by(telefono=e.usuario_reserva).first()
                            if usuario:
                                enviar_alerta_personalizada(usuario.chat_id, e.id, minutos)
                                e.alerta_enviada = True
                    else:
                        e.hora_inicio = ahora
                        e.tiempo_transcurrido = 0
                else:
                    e.hora_inicio = None
                    e.tiempo_transcurrido = 0
                    e.alerta_enviada = False
                e.ultima_actualizacion = ahora
            db.session.commit()
        time.sleep(0.5)

def inicializar_bd():
    with app.app_context():
        db.drop_all()
        db.create_all()
        espacios = [
            Espacio(id=1, ocupado=False, reservado=False, disponible=True),
            Espacio(id=2, ocupado=False, reservado=False, disponible=True),
            Espacio(id=3, ocupado=True, reservado=True, disponible=False, hora_inicio=datetime.now()),
            Espacio(id=4, ocupado=False, reservado=False, disponible=True),
        ]
        db.session.add_all(espacios)
        db.session.commit()
        print("✅ Base de datos inicializada")

try:
    arduino = abrir_serial()
except Exception as e:
    print(f"⚠️ No se pudo conectar con Arduino: {e}")
    arduino = None

PRECIO_POR_HORA = 10000
TIEMPO_GRATIS_MINUTOS = 60

if __name__ == '__main__':
    inicializar_bd()
    threading.Thread(target=verificar_tiempos_ocupacion, daemon=True).start()
    app.run(debug=True)