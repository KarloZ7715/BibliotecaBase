from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import get_db

router = APIRouter(
    prefix="/detallepedido",
    tags=["DetallePedidos"],
)


@router.post("/", response_model=schemas.DetallePedido)
def crear_detallepedido(
    detallepedido: schemas.DetallePedidoCreate, db: Session = Depends(get_db)
):
    db_detallepedido = models.DetallePedido(**detallepedido.dict())
    db.add(db_detallepedido)
    db.commit()
    db.refresh(db_detallepedido)
    return db_detallepedido


@router.get("/{detallepedido_id}", response_model=schemas.DetallePedido)
def leer_detallepedido(detallepedido_id: int, db: Session = Depends(get_db)):
    detallepedido = (
        db.query(models.DetallePedido)
        .filter(models.DetallePedido.id_detallepedido == detallepedido_id)
        .first()
    )
    if detallepedido is None:
        raise HTTPException(status_code=404, detail="DetallePedido no encontrado")
    return detallepedido


@router.put("/{detallepedido_id}", response_model=schemas.DetallePedido)
def actualizar_detallepedido(
    detallepedido_id: int,
    detallepedido: schemas.DetallePedidoCreate,
    db: Session = Depends(get_db),
):
    db_detallepedido = (
        db.query(models.DetallePedido)
        .filter(models.DetallePedido.id_detallepedido == detallepedido_id)
        .first()
    )
    if db_detallepedido is None:
        raise HTTPException(status_code=404, detail="DetallePedido no encontrado")
    for key, value in detallepedido.dict().items():
        setattr(db_detallepedido, key, value)
    db.commit()
    db.refresh(db_detallepedido)
    return db_detallepedido


@router.delete("/{detallepedido_id}")
def eliminar_detallepedido(detallepedido_id: int, db: Session = Depends(get_db)):
    detallepedido = (
        db.query(models.DetallePedido)
        .filter(models.DetallePedido.id_detallepedido == detallepedido_id)
        .first()
    )
    if detallepedido is None:
        raise HTTPException(status_code=404, detail="DetallePedido no encontrado")
    db.delete(detallepedido)
    db.commit()
    return {"detail": "DetallePedido eliminado correctamente"}
