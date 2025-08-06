from sqlalchemy import Column, Integer, String
from database import Base

class EmocionDB(Base):
    __tablename__ = "emociones"

    id = Column(Integer, primary_key=True, index=True)
    emocion = Column(String, index=True)
    mensaje = Column(String)
