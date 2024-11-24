from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import schemas
from database import get_db
from dependencies import get_current_user
from typing import List


router = APIRouter(
    prefix="/carrito",
    tags=["Carrito"],
)


@router.post("/", response_model=schemas.Carrito)
def agregar_al_carrito(
    item: schemas.CarritoCreate,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user),
):
    db_item = (
        db.query(models.Carrito)
        .filter(
            models.Carrito.id_usuario == usuario.id_usuario,
            models.Carrito.id_libro == item.id_libro,
        )
        .first()
    )
    if db_item:
        db_item.cantidad += item.cantidad
    else:
        db_item = models.Carrito(
            id_usuario=usuario.id_usuario,
            id_libro=item.id_libro,
            cantidad=item.cantidad,
        )
        db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.get("/", response_model=List[schemas.Carrito])
def obtener_carrito(
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user),
):
    carrito = (
        db.query(models.Carrito)
        .filter(models.Carrito.id_usuario == usuario.id_usuario)
        .all()
    )
    return carrito


@router.delete("{id_carrito}", response_model=schemas.Carrito)
def eliminar_del_carrito(
    id_carrito: int,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user),
):
    db_item = (
        db.query(models.Carrito)
        .filter(
            models.Carrito.id_carrito == id_carrito,
            models.Carrito.id_usuario == usuario.id_usuario,
        )
        .first()
    )
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item no encontrado en el carrito")
    db.delete(db_item)
    db.commit()
    return db_item
