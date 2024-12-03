from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from decimal import Decimal
from datetime import date, datetime


class AutorBase(BaseModel):
    nombre: str
    biografia: Optional[str] = None
    fecha_nacimiento: Optional[date] = None


class AutorCreate(AutorBase):
    pass


class Autor(AutorBase):
    id_autor: int

    class Config:
        orm_mode = True


class CategoriaBase(BaseModel):
    nombre_categoria: str


class CategoriaCreate(CategoriaBase):
    pass


class Categoria(CategoriaBase):
    id_categoria: int

    class Config:
        orm_mode = True


class UsuarioBase(BaseModel):
    nombre: str
    correo: EmailStr
    direccion: Optional[str] = None
    telefono: Optional[str] = None


class UsuarioCreate(UsuarioBase):
    contraseña: str


class Usuario(UsuarioBase):
    id_usuario: int
    rol: str
    fecha_registro: datetime

    class Config:
        orm_mode = True


class LibroBase(BaseModel):
    titulo: str
    descripcion: Optional[str] = None
    precio: float
    stock: int = 0
    id_autor: Optional[int] = None
    id_categoria: Optional[int] = None
    imagen_url: Optional[str] = None
    fecha_publicacion: Optional[date] = None
    isbn: Optional[str] = None


class LibroCreate(LibroBase):
    pass


class Libro(LibroBase):
    id_libro: int
    autor: Optional[Autor] = None
    categoria: Optional[Categoria] = None

    class Config:
        orm_mode = True


class CarritoBase(BaseModel):
    id_libro: int
    cantidad: Optional[int] = 1


class CarritoCreate(CarritoBase):
    pass


class Carrito(CarritoBase):
    id_carrito: int
    id_usuario: int
    fecha_agregado: datetime
    libro: Optional[Libro] = None

    class Config:
        orm_mode = True


class DetallePedidoBase(BaseModel):
    id_pedido: int
    id_libro: int
    cantidad: int = 1
    precio_unitario: Decimal


class DetallePedidoCreate(BaseModel):
    id_libro: int
    cantidad: int
    precio_unitario: Decimal


class DetallePedido(DetallePedidoBase):
    id_detallepedido: int
    libro: Optional[Libro] = None

    class Config:
        orm_mode = True


class PedidoBase(BaseModel):
    id_usuario: int
    total: Decimal
    estado: Optional[str] = "En proceso"


class PedidoCreate(PedidoBase):
    detallepedido: List[DetallePedidoCreate]


class Pedido(PedidoBase):
    id_pedido: int
    fecha_pedido: datetime
    detallepedido: List[DetallePedido] = []

    class Config:
        orm_mode = True


class ValoracionBase(BaseModel):
    id_libro: int
    valoracion: int = Field(..., ge=1, le=5)


class ValoracionCreate(ValoracionBase):
    pass


class Valoracion(ValoracionBase):
    id_valoracion: int
    id_usuario: int
    fecha_valoracion: datetime
    usuario: Usuario

    class Config:
        orm_mode = True


class TarjetaBase(BaseModel):
    numero_tarjeta: str
    fecha_expiracion: date
    tipo: str
    nombre_titular: str


class TarjetaCreate(TarjetaBase):
    pass


class Tarjeta(TarjetaBase):
    id_tarjeta: int
    id_usuario: int

    class Config:
        orm_mode = True


class Login(BaseModel):
    correo: EmailStr
    contraseña: str


class RegistroBase(BaseModel):
    accion: str
    detalles: Optional[str] = None


class RegistroCreate(RegistroBase):
    pass


class Registro(RegistroBase):
    id_registro: int
    id_usuario: int
    fecha: datetime
    hora: Optional[datetime] = None

    class Config:
        orm_mode = True
