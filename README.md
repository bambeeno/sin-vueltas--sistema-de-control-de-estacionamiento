# Sistema de Estacionamiento Inteligente (MVP)

**MVP funcional** desarrollado como prueba de concepto para un sistema de gestión de estacionamientos automatizado.  
El proyecto integra hardware real (sensores y placas Arduino) con una aplicación web ligera creada en **Flask**, **SQLAlchemy**, **SQLite/MySQL** y **Tailwind CSS**.

---

## Descripción general

Este proyecto busca demostrar la **viabilidad técnica y operativa** de un sistema de estacionamiento inteligente, capaz de administrar reservas, espacios y facturación, comunicándose con hardware físico a través de Arduino.

> *El desarrollo se enfocó en construir un MVP (Minimum Viable Product), utilizando componentes y placas disponibles para validar la idea con el menor costo y máxima funcionalidad real.*
---

## Características principales

-Gestión de espacios disponibles y ocupados  
-Registro de usuarios y reservas  
-Generación automática de facturas  
-Comunicación en tiempo real con sensores Arduino  
-Interfaz web simple, funcional y optimizada con **Tailwind CSS**  
-Arquitectura modular y ampliable  

---

## Tecnologías utilizadas

| Categoría | Tecnologías |
|------------|-------------|
| **Backend** | Python, Flask, SQLAlchemy |
| **Base de datos** | SQLite / MySQL |
| **Frontend** | HTML + Tailwind CSS *(sin JavaScript directo)* |
| **Hardware** | Arduino + sensores físicos disponibles |
| **Enfoque** | MVP - Minimum Viable Product |

---

## Instalación y configuración

Sigue estos pasos para correr el proyecto localmente

###  Clonar el repositorio
```bash
git clone https://github.com/bambeeno/estacionamiento.git
cd estacionamiento

```
### Crear entorno virtual
``` bash
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows
```

Instalar dependencias
```bash
pip install -r requirements.txt
```
Inicializar la base de datos
```bash
flask shell
>>> from models import db
>>> db.create_all()
>>> exit()
```
Ejecutar la aplicación
```bash
flask run
```
Luego abre en tu navegador:
 http://127.0.0.1:5000

Estructura del proyecto
```
estacionamiento/
│
├── app.py                # Punto de entrada principal (Flask)
├── conexion.py           # Comunicación serial con Arduino
├── models.py             # Modelos de base de datos (SQLAlchemy)
├── templates/            # Vistas HTML con Tailwind
├── static/               # Archivos estáticos (CSS, imágenes)
├── estacionamiento.db    # Base de datos local (SQLite)
├── requirements.txt      # Dependencias del proyecto
└── README.md             # Documentación del repositorio
```

### **Integración con Arduino y sensores**

-El archivo conexion.py maneja la comunicación serial entre la aplicación Flask y la placa Arduino.

Esta capa permite:

-Detectar automáticamente la ocupación de los espacios (mediante sensores).

-Activar o desactivar barreras físicas según las reservas o entradas registradas.

-Sincronizar el estado en tiempo real con la base de datos del sistema.

-El sistema fue probado con sensores disponibles comercialmente, adaptados a las necesidades del prototipo.

 ### **Flujo básico de uso**

-El usuario ingresa a la aplicación web y consulta los espacios disponibles.

-Realiza una reserva y obtiene confirmación.

-Al llegar, el sensor detecta el vehículo y el Arduino envía la señal a Flask.

-El sistema marca la entrada y genera la factura al finalizar la estancia.

 ### **Filosofía del proyecto**

> ***“Un prototipo funcional vale más que mil diagramas.”*** 

## **Este MVP fue desarrollado para:**

-Validar la interacción entre software y hardware real.

-Comprobar la fiabilidad de los sensores disponibles.

-Servir de base para una futura versión escalable con paneles de control y API REST.

## **Contribución**

¡Las ideas y aportes son bienvenidos!
Puedes colaborar con mejoras de código, documentación o nuevas integraciones de hardware.

Haz un fork del repositorio

Crea una nueva rama: git checkout -b feature/nueva-funcionalidad

## Realiza tus cambios

Envía un pull request con una descripción clara

### **Autores**

***Bambeeno***
📧 alejandroruizdiazmoreno@gmail.com

🌐 LinkedIn
`www.linkedin.com/in/alejandro-ruiz-diaz-moreno-712537210

🐙 GitHub
Bambeeno

***Norixpy***

🐙 GitHub
Norixpy
***

📄 Licencia

Este proyecto está bajo la licencia MIT.
Consulta el archivo LICENSE
 para más detalles.


