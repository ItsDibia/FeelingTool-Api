from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas import Emocion
from models import EmocionDB
from database import SessionLocal, engine, Base
from collections import Counter

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Permitir acceso desde el frontend (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia esto por el dominio de tu front en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "API de emociones funcionando"}

@app.post("/emocion")
def crear_emocion(emocion: Emocion):
    db = SessionLocal()
    db_emocion = EmocionDB(emocion=emocion.emocion, mensaje=emocion.mensaje)
    db.add(db_emocion)
    db.commit()
    db.refresh(db_emocion)
    db.close()
    return {
        "id": db_emocion.id,
        "emocion": db_emocion.emocion,
        "mensaje": db_emocion.mensaje
    }

@app.get("/emociones")
def obtener_emociones():
    db = SessionLocal()
    emociones = db.query(EmocionDB).all()
    db.close()
    return emociones

@app.get("/emocion/{id}")
def obtener_emocion(id: int):
    db = SessionLocal()
    emocion = db.query(EmocionDB).filter(EmocionDB.id == id).first()
    db.close()
    if not emocion:
        raise HTTPException(status_code=404, detail="Emocion no encontrada")
    return emocion

@app.put("/emocion/{id}")
def actualizar_emocion(id: int, emocion: Emocion):
    db = SessionLocal()
    db_emocion = db.query(EmocionDB).filter(EmocionDB.id == id).first()
    if not db_emocion:
        db.close()
        raise HTTPException(status_code=404, detail="Emocion no encontrada")
    db_emocion.emocion = emocion.emocion
    db_emocion.mensaje = emocion.mensaje
    db.commit()
    db.refresh(db_emocion)
    db.close()
    return db_emocion

@app.delete("/emocion/{id}")
def eliminar_emocion(id: int):
    db = SessionLocal()
    emocion = db.query(EmocionDB).filter(EmocionDB.id == id).first()
    if not emocion:
        db.close()
        raise HTTPException(status_code=404, detail="Emocion no encontrada")
    db.delete(emocion)
    db.commit()
    db.close()
    return {"message": "Emocion eliminada"}

# NUEVA RUTA /resultado
@app.get("/resultado")
def obtener_resultado():
    db = SessionLocal()
    emociones = db.query(EmocionDB).all()
    db.close()

    if not emociones:
        return {
            "total": 0,
            "emocion_frecuente": None,
            "ultimo_mensaje": None
        }

    total = len(emociones)
    conteo = Counter([e.emocion for e in emociones])
    emocion_frecuente = conteo.most_common(1)[0][0]
    ultimo_mensaje = emociones[-1].mensaje

    return {
        "total": total,
        "emocion_frecuente": emocion_frecuente,
        "ultimo_mensaje": ultimo_mensaje
    }
