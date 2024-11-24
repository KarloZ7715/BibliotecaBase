from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from dependencies import get_db, get_current_user

router = APIRouter(
    prefix="/autores",
    tags=["Autores"],
)


@router.get("/", response_model=List[schemas.Autor])
def obtener_autores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    autores = db.query(models.Autor).offset(skip).limit(limit).all()
    return autores


@router.get("/{id_autor}", response_model=schemas.Autor)
def obtener_autor(id_autor: int, db: Session = Depends(get_db)):
    autor = db.query(models.Autor).filter(models.Autor.id_autor == id_autor).first()
    if not autor:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    return autor


@router.post("/", response_model=schemas.Autor)
def crear_autor(
    autor: schemas.AutorCreate,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user),
):
    if usuario.rol != "admin":
        raise HTTPException(
            status_code=403, detail="No tienes permiso para crear autores"
        )
    db_autor = models.Autor(**autor.dict())
    db.add(db_autor)
    db.commit()
    db.refresh(db_autor)
    return db_autor


@router.put("/{id_autor}", response_model=schemas.Autor)
def actualizar_autor(
    id_autor: int,
    autor: schemas.AutorCreate,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user),
):
    if usuario.rol != "admin":
        raise HTTPException(
            status_code=403, detail="No tienes permiso para actualizar autores"
        )
    db_autor = db.query(models.Autor).filter(models.Autor.id_autor == id_autor).first()
    if not db_autor:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    for key, value in autor.dict().items():
        setattr(db_autor, key, value)
    db.commit()
    db.refresh(db_autor)
    return db_autor


@router.delete("/{id_autor}", response_model=schemas.Autor)
def eliminar_autor(
    id_autor: int,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user),
):
    if usuario.rol != "admin":
        raise HTTPException(
            status_code=403, detail="No tienes permiso para eliminar autores"
        )
    db_autor = db.query(models.Autor).filter(models.Autor.id_autor == id_autor).first()
    if not db_autor:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    db.delete(db_autor)
    db.commit()
    return db_autor
