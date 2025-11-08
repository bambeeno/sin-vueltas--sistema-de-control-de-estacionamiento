import serial
import serial.tools.list_ports
import time

# Buscar el puerto donde está conectado el Arduino
def buscar_puerto():
    puertos = serial.tools.list_ports.comports()
    for p in puertos:
        desc = (p.description or "").lower()
        if 'arduino' in desc or 'usb' in desc or 'serial' in desc:
            return p.device
    return None

# Abrir el puerto serie con manejo de errores
def abrir_serial(puerto=None, baud=9600, timeout=1):
    if puerto is None:
        puerto = buscar_puerto()
    if not puerto:
        raise RuntimeError("❌ No se encontró puerto serie de Arduino")

    print(f"🔌 Conectando al puerto {puerto}...")
    try:
        ser = serial.Serial(puerto, baud, timeout=timeout)
        time.sleep(0.05)  # Esperar a que el Arduino reinicie
        return ser
    except serial.SerialException as e:
        raise RuntimeError(f"❌ No se pudo abrir el puerto {puerto}: {e}")