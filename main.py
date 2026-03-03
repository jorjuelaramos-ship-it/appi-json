from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import psycopg2
import os
import secrets

app = FastAPI()
security = HTTPBasic()

# 🔹 Usuario y contraseña (mejor ponerlos en variables de entorno en Render)
API_USER = os.environ.get("API_USER")
API_PASSWORD = os.environ.get("API_PASSWORD")

DATABASE_URL = os.environ.get("DATABASE_URL")

class Registro(BaseModel):
    nombre: str
    correo: str
    mensaje: str

def get_conn():
    return psycopg2.connect(DATABASE_URL)

# 🔐 Función para validar usuario y contraseña
def validar_usuario(credentials: HTTPBasicCredentials = Depends(security)):
    correct_user = secrets.compare_digest(credentials.username, API_USER)
    correct_pass = secrets.compare_digest(credentials.password, API_PASSWORD)

    if not (correct_user and correct_pass):
        raise HTTPException(status_code=401, detail="No autorizado")

    return credentials.username

# POST protegido
@app.post("/api/ingresar")
async def ingresar_datos(
    registro: Registro,
    username: str = Depends(validar_usuario)
):
    try:
        conn = get_conn()
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS registro (
                id INT PRIMARY KEY,
                nombre TEXT,
                correo TEXT,
                mensaje TEXT
            );
        """)

        cur.execute("""
            INSERT INTO registro (id, nombre, correo, mensaje)
            VALUES (1, %s, %s, %s)
            ON CONFLICT (id) DO UPDATE SET
                nombre = EXCLUDED.nombre,
                correo = EXCLUDED.correo,
                mensaje = EXCLUDED.mensaje;
        """, (registro.nombre, registro.correo, registro.mensaje))

        conn.commit()
        cur.close()
        conn.close()

        return {"mensaje": "Datos guardados correctamente"}

    except Exception as e:
        return {"error": str(e)}

