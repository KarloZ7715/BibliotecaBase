from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from dependencies import get_db, get_current_user
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"],
)


@router.post("/", response_model=schemas.Pedido)
def crear_pedido(pedido: schemas.PedidoCreate, db: Session = Depends(get_db)):
    try:
        db_pedido = models.Pedido(
            id_usuario=pedido.id_usuario, total=pedido.total, estado=pedido.estado
        )
        db.add(db_pedido)
        db.commit()
        db.refresh(db_pedido)

        for detalle in pedido.detallepedido:
            db_detalle = models.DetallePedido(
                id_pedido=db_pedido.id_pedido,
                id_libro=detalle.id_libro,
                cantidad=detalle.cantidad,
                precio_unitario=detalle.precio_unitario,
            )
            db.add(db_detalle)

        db.commit()
        db.refresh(db_pedido)
        return db_pedido
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al crear el pedido")


@router.get("/", response_model=List[schemas.Pedido])
def obtener_pedidos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user),
):
    if usuario.rol == "admin":
        pedidos = db.query(models.Pedido).offset(skip).limit(limit).all()
    else:
        pedidos = (
            db.query(models.Pedido)
            .filter(models.Pedido.id_usuario == usuario.id_usuario)
            .offset(skip)
            .limit(limit)
            .all()
        )
    return pedidos


@router.get("/{pedido_id}", response_model=schemas.Pedido)
def leer_pedido(pedido_id: int, db: Session = Depends(get_db)):
    pedido = (
        db.query(models.Pedido).filter(models.Pedido.id_pedido == pedido_id).first()
    )
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido


@router.put("/{id_pedido}", response_model=schemas.Pedido)
def actualizar_pedido(
    id_pedido: int,
    pedido: schemas.PedidoCreate,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user),
):
    if usuario.rol != "admin":
        raise HTTPException(
            status_code=403, detail="Solo los administradores pueden actualizar pedidos"
        )
    db_pedido = (
        db.query(models.Pedido).filter(models.Pedido.id_pedido == id_pedido).first()
    )
    if not db_pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    db_pedido.total = pedido.total
    db_pedido.estado = pedido.estado
    db.commit()
    db.refresh(db_pedido)
    return db_pedido


@router.delete("/{id_pedido}", response_model=schemas.Pedido)
def eliminar_pedido(
    id_pedido: int,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user),
):
    if usuario.rol != "admin":
        raise HTTPException(
            status_code=403, detail="Solo los administradores pueden eliminar pedidos"
        )
    db_pedido = (
        db.query(models.Pedido).filter(models.Pedido.id_pedido == id_pedido).first()
    )
    if not db_pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    db.delete(db_pedido)
    db.commit()
    return db_pedido
