# test_conexion.py
import conexion

try:
    ser = conexion.abrir_serial()
    print(f"✅ Conectado al puerto {ser.port}. Esperando datos...\n")

    while True:
        if ser.in_waiting:
            linea = ser.readline().decode(errors='ignore').strip()
            print("📨 Arduino dice:", linea)
except Exception as e:
    print("❌ Error al conectar:", e)
    