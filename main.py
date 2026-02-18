from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import json

app = FastAPI()

# Modelo del JSON esperado
class Registro(BaseModel):
    nombre: str
    monto: float
    descripcion: str | None = None

@app.post("/api/ingresar")
async def ingresar_datos(registro: Registro):

    data = registro.dict()
    data["fecha_recibido"] = datetime.now().isoformat()

    # Guardar en archivo
    with open("datos.json", "a") as f:
        f.write(json.dumps(data) + "\n")

    return {
        "mensaje": "Datos recibidos correctamente",
        "data": data
    }
