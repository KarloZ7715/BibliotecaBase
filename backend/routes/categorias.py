from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from dependencies import get_db, get_current_user

router = APIRouter(
    prefix="/categorias",
    tags=["Categorías"],
)


@router.post("/", response_model=schemas.Categoria)
def crear_categoria(
    categoria: schemas.CategoriaCreate,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user),
):
    if usuario.rol != "admin":
        raise HTTPException(
            status_code=403, detail="No tienes permiso para crear categorías"
        )
    db_categoria = models.Categoria(**categoria.dict())
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria


@router.get("/", response_model=List[schemas.Categoria])
def obtener_categorias(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categorias = db.query(models.Categoria).offset(skip).limit(limit).all()
    return categorias


@router.get("/{id_categoria}", response_model=schemas.Categoria)
def obtener_categoria(id_categoria: int, db: Session = Depends(get_db)):
    categoria = (
        db.query(models.Categoria)
        .filter(models.Categoria.id_categoria == id_categoria)
        .first()
    )
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria


@router.put("/{id_categoria}", response_model=schemas.Categoria)
def actualizar_categoria(
    id_categoria: int,
    categoria: schemas.CategoriaCreate,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user),
):
    if usuario.rol != "admin":
        raise HTTPException(
            status_code=403, detail="No tienes permiso para actualizar categorías"
        )
    db_categoria = (
        db.query(models.Categoria)
        .filter(models.Categoria.id_categoria == id_categoria)
        .first()
    )
    if not db_categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    for key, value in categoria.dict().items():
        setattr(db_categoria, key, value)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria


@router.delete("/{id_categoria}", response_model=schemas.Categoria)
def eliminar_categoria(
    id_categoria: int,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user),
):
    if usuario.rol != "admin":
        raise HTTPException(
            status_code=403, detail="No tienes permiso para eliminar categorías"
        )
    db_categoria = (
        db.query(models.Categoria)
        .filter(models.Categoria.id_categoria == id_categoria)
        .first()
    )
    if not db_categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    db.delete(db_categoria)
    db.commit()
    return db_categoria
