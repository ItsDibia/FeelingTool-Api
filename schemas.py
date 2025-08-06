from pydantic import BaseModel

class Emocion(BaseModel):
    emocion: str
    mensaje: str  
