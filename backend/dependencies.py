from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
import models
from database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="No autenticado")
    usuario = (
        db.query(models.Usuario).filter(models.Usuario.id_usuario == user_id).first()
    )
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    return usuario
