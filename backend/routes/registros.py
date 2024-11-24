from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from dependencies import get_db, get_current_user

router = APIRouter(
    prefix="/registros",
    tags=["Registros"],
)


@router.get("/", response_model=List[schemas.Registro])
def obtener_registros(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user),
):
    if usuario.rol != "admin":
        raise HTTPException(
            status_code=403, detail="No tienes permiso para ver registros"
        )
    registros = db.query(models.Registro).offset(skip).limit(limit).all()
    return registros
