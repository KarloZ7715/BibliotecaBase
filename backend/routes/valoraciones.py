from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
import models
import schemas
from dependencies import get_db, get_current_user

router = APIRouter(
    prefix="/valoraciones",
    tags=["Valoraciones"],
)


@router.post("/", response_model=schemas.Valoracion)
def crear_valoracion(
    valoracion: schemas.ValoracionCreate,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user),
):
    detalle = (
        db.query(models.DetallePedido)
        .join(models.Pedido)
        .filter(
            models.DetallePedido.id_libro == valoracion.id_libro,
            models.Pedido.id_usuario == usuario.id_usuario,
        )
        .first()
    )
    if not detalle:
        raise HTTPException(
            status_code=403, detail="Debes comprar el libro antes de poder valorarlo."
        )
    valoracion_existente = (
        db.query(models.Valoracion)
        .filter(
            models.Valoracion.id_libro == valoracion.id_libro,
            models.Valoracion.id_usuario == usuario.id_usuario,
        )
        .first()
    )
    if valoracion_existente:
        raise HTTPException(status_code=400, detail="Ya has valorado este libro.")
    if usuario.rol != "cliente":
        raise HTTPException(
            status_code=403, detail="Solo los clientes pueden crear valoraciones"
        )
    db_valoracion = models.Valoracion(
        **valoracion.dict(), id_usuario=usuario.id_usuario
    )
    db.add(db_valoracion)
    db.commit()
    db.refresh(db_valoracion)
    return db_valoracion


@router.get("/", response_model=List[schemas.Valoracion])
def obtener_valoraciones(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    valoraciones = db.query(models.Valoracion).offset(skip).limit(limit).all()
    return valoraciones


@router.get("/{id_valoracion}", response_model=schemas.Valoracion)
def obtener_valoracion(id_valoracion: int, db: Session = Depends(get_db)):
    valoracion = (
        db.query(models.Valoracion)
        .filter(models.Valoracion.id_valoracion == id_valoracion)
        .first()
    )
    if not valoracion:
        raise HTTPException(status_code=404, detail="Valoración no encontrada")
    return valoracion


@router.get("/libro/{id_libro}", response_model=List[schemas.Valoracion])
def obtener_valoraciones_libro(id_libro: int, db: Session = Depends(get_db)):
    valoraciones = (
        db.query(models.Valoracion).filter(models.Valoracion.id_libro == id_libro).all()
    )
    return valoraciones


@router.get("/libro/{id_libro}/promedio", response_model=float)
def obtener_promedio_valoraciones(id_libro: int, db: Session = Depends(get_db)):
    promedio = (
        db.query(func.avg(models.Valoracion.valoracion))
        .filter(models.Valoracion.id_libro == id_libro)
        .scalar()
    )
    if promedio is None:
        return 0.0
    return float(promedio)


@router.put("/{id_valoracion}", response_model=schemas.Valoracion)
def actualizar_valoracion(
    id_valoracion: int,
    valoracion: schemas.ValoracionCreate,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user),
):
    db_valoracion = (
        db.query(models.Valoracion)
        .filter(
            models.Valoracion.id_valoracion == id_valoracion,
            models.Valoracion.id_usuario == usuario.id_usuario,
        )
        .first()
    )
    if not db_valoracion:
        raise HTTPException(status_code=404, detail="Valoración no encontrada")
    db_valoracion.valoracion = valoracion.valoracion
    db.commit()
    db.refresh(db_valoracion)
    return db_valoracion


@router.delete("/{id_valoracion}")
def eliminar_valoracion(
    id_valoracion: int,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user),
):
    db_valoracion = (
        db.query(models.Valoracion)
        .filter(
            models.Valoracion.id_valoracion == id_valoracion,
            models.Valoracion.id_usuario == usuario.id_usuario,
        )
        .first()
    )
    if not db_valoracion:
        raise HTTPException(status_code=404, detail="Valoración no encontrada")
    db.delete(db_valoracion)
    db.commit()
    return {"detail": "Valoración eliminada correctamente"}
