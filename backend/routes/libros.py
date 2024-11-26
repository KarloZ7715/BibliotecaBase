from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import List
import models
import schemas
from dependencies import get_db, get_current_user
import random

router = APIRouter(
    prefix="/libros",
    tags=["Libros"],
)


@router.post("/", response_model=schemas.Libro)
def crear_libro(
    libro: schemas.LibroCreate,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user),
):
    if usuario.rol != "admin":
        raise HTTPException(
            status_code=403, detail="No tienes permiso para crear libros"
        )
    db_libro = models.Libro(**libro.dict())
    db.add(db_libro)
    db.commit()
    db.refresh(db_libro)
    return db_libro


@router.get("/", response_model=List[schemas.Libro])
def obtener_libros(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    libros = db.query(models.Libro).offset(skip).limit(limit).all()
    return libros


@router.get("/random", response_model=List[schemas.Libro])
def get_random_books(limit: int = Query(5, ge=1, le=10), db: Session = Depends(get_db)):
    total_books = db.query(models.Libro).count()
    if total_books == 0:
        return []
    limit = min(limit, total_books)
    libros = db.query(models.Libro).options(joinedload(models.Libro.autor)).all()
    random_books = random.sample(libros, limit)
    return random_books


@router.get("/buscar", response_model=List[schemas.Libro])
def buscar_libros(query: str, filter: str = "Todo", db: Session = Depends(get_db)):
    if filter == "Título":
        libros = (
            db.query(models.Libro)
            .options(joinedload(models.Libro.autor), joinedload(models.Libro.categoria))
            .filter(models.Libro.titulo.ilike(f"%{query}%"))
            .all()
        )
    elif filter == "Autor":
        libros = (
            db.query(models.Libro)
            .join(models.Autor)
            .options(joinedload(models.Libro.autor), joinedload(models.Libro.categoria))
            .filter(models.Autor.nombre.ilike(f"%{query}%"))
            .all()
        )
    elif filter == "Género":
        libros = (
            db.query(models.Libro)
            .join(models.Categoria)
            .options(joinedload(models.Libro.autor), joinedload(models.Libro.categoria))
            .filter(models.Categoria.nombre_categoria.ilike(f"%{query}%"))
            .all()
        )
    else:
        libros = (
            db.query(models.Libro)
            .join(models.Autor)
            .join(models.Categoria)
            .options(joinedload(models.Libro.autor), joinedload(models.Libro.categoria))
            .filter(
                (models.Libro.titulo.ilike(f"%{query}%"))
                | (models.Autor.nombre.ilike(f"%{query}%"))
                | (models.Categoria.nombre_categoria.ilike(f"%{query}%"))
            )
            .all()
        )
    return libros


@router.get("/{id_libro}", response_model=schemas.Libro)
def obtener_libro(id_libro: int, db: Session = Depends(get_db)):
    libro = (
        db.query(models.Libro)
        .options(joinedload(models.Libro.autor), joinedload(models.Libro.categoria))
        .filter(models.Libro.id_libro == id_libro)
        .first()
    )
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro


@router.put("/{id_libro}", response_model=schemas.Libro)
def actualizar_libro(
    id_libro: int,
    libro: schemas.LibroCreate,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user),
):
    if usuario.rol != "admin":
        raise HTTPException(
            status_code=403, detail="No tienes permiso para actualizar libros"
        )
    db_libro = db.query(models.Libro).filter(models.Libro.id_libro == id_libro).first()
    if not db_libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    for key, value in libro.dict().items():
        setattr(db_libro, key, value)
    db.commit()
    db.refresh(db_libro)
    return db_libro


@router.delete("/{id_libro}", response_model=schemas.Libro)
def eliminar_libro(
    id_libro: int,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user),
):
    if usuario.rol != "admin":
        raise HTTPException(
            status_code=403, detail="No tienes permiso para eliminar libros"
        )
    db_libro = db.query(models.Libro).filter(models.Libro.id_libro == id_libro).first()
    if not db_libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    db.delete(db_libro)
    db.commit()
    return db_libro
