from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Carrito, Libro
from schemas import Carrito as CarritoSchema
from dependencies import get_current_user


router = APIRouter(
    prefix="/carrito",
    tags=["Carrito"],
)


@router.get("/", response_model=List[CarritoSchema])
def obtener_carrito_actual(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    carrito_items = (
        db.query(Carrito).filter(Carrito.id_usuario == current_user.id_usuario).all()
    )
    return carrito_items


@router.post("/agregar", response_model=CarritoSchema)
def agregar_al_carrito(
    id_libro: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    carrito_item = (
        db.query(Carrito)
        .filter(
            Carrito.id_usuario == current_user.id_usuario, Carrito.id_libro == id_libro
        )
        .first()
    )
    if carrito_item:
        carrito_item.cantidad += 1
        carrito_item.fecha_agregado = datetime.now()
    else:
        nuevo_item = Carrito(
            id_usuario=current_user.id_usuario,
            id_libro=id_libro,
            cantidad=1,
            fecha_agregado=datetime.now(),
        )
        db.add(nuevo_item)
    db.commit()
    db.refresh(carrito_item if carrito_item else nuevo_item)
    return carrito_item if carrito_item else nuevo_item


@router.put("/actualizar", response_model=CarritoSchema)
def actualizar_cantidad_carrito(
    id_libro: int,
    cantidad: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    if cantidad < 0:
        raise HTTPException(status_code=400, detail="La cantidad no puede ser negativa")

    carrito_item = (
        db.query(Carrito)
        .filter(
            Carrito.id_usuario == current_user.id_usuario, Carrito.id_libro == id_libro
        )
        .first()
    )
    if not carrito_item:
        raise HTTPException(status_code=404, detail="El ítem no está en el carrito")

    if cantidad == 0:
        db.delete(carrito_item)
    else:
        carrito_item.cantidad = cantidad
        carrito_item.fecha_agregado = datetime.now()

    db.commit()
    return carrito_item


@router.delete("/eliminar", response_model=dict)
def eliminar_del_carrito(
    id_libro: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    carrito_item = (
        db.query(Carrito)
        .filter(
            Carrito.id_usuario == current_user.id_usuario, Carrito.id_libro == id_libro
        )
        .first()
    )
    if not carrito_item:
        raise HTTPException(status_code=404, detail="El ítem no está en el carrito")

    db.delete(carrito_item)
    db.commit()
    return {"detail": "Ítem eliminado del carrito"}


@router.delete("/vaciar", response_model=dict)
def vaciar_carrito(
    db: Session = Depends(get_db), current_user: int = Depends(get_current_user)
):
    db.query(Carrito).filter(Carrito.id_usuario == current_user.id_usuario).delete()
    db.commit()
    return {"detail": "Carrito vaciado"}
