from fastapi import FastAPI
from pydantic import BaseModel
import json
import os

app = FastAPI()

class Registro(BaseModel):
    nombre: str
    correo: str
    mensaje: str

# POST - Guarda datos
@app.post("/api/ingresar")
async def ingresar_datos(registro: Registro):
    with open("datos.json", "w") as f:
        json.dump(registro.dict(), f)

    return {"mensaje": "Datos guardados correctamente"}

# GET - Devuelve datos para Power BI
@app.get("/api/datos")
async def obtener_datos():
    if os.path.exists("datos.json"):
        with open("datos.json", "r") as f:
            data = json.load(f)
        return data
    return {"mensaje": "No hay datos aún"}
