from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime, timezone
from sqlalchemy import CheckConstraint
from sqlalchemy import (
    Column,
    Enum,
    Time,
    Integer,
    String,
    Text,
    DateTime,
    Date,
    DECIMAL,
    ForeignKey,
)


class Autor(Base):
    __tablename__ = "autores"
    id_autor = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    biografia = Column(Text, nullable=True)
    fecha_nacimiento = Column(Date, nullable=True)
    libros = relationship("Libro", back_populates="autor")


class Libro(Base):
    __tablename__ = "libros"
    id_libro = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(200), nullable=False)
    descripcion = Column(Text, nullable=True)
    precio = Column(DECIMAL(10, 2), nullable=False)
    stock = Column(Integer, default=0)
    id_autor = Column(Integer, ForeignKey("autores.id_autor"), nullable=True)
    id_categoria = Column(Integer, ForeignKey("categorias.id_categoria"), nullable=True)
    imagen_url = Column(String(255), nullable=True)
    fecha_publicacion = Column(Date, nullable=True)
    isbn = Column(String(20), nullable=True)
    autor = relationship("Autor", back_populates="libros")
    categoria = relationship("Categoria", back_populates="libros")
    valoraciones = relationship("Valoracion", back_populates="libro")
    carrito = relationship("Carrito", back_populates="libro")
    detallepedido = relationship("DetallePedido", back_populates="libro")


class Usuario(Base):
    __tablename__ = "usuarios"
    id_usuario = Column(Integer, primary_key=True, index=True)
    rol = Column(Enum("admin", "cliente"), default="cliente", nullable=False)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(100), unique=True, nullable=False)
    contraseña = Column(String(255), nullable=False)
    direccion = Column(Text, nullable=True)
    telefono = Column(String(15), nullable=True)
    fecha_registro = Column(DateTime, default=datetime.now(timezone.utc))
    pedidos = relationship("Pedido", back_populates="usuario")
    carrito = relationship("Carrito", back_populates="usuario")
    valoraciones = relationship("Valoracion", back_populates="usuario")
    tarjetas = relationship("Tarjeta", back_populates="usuario")
    registro = relationship("Registro", back_populates="usuario")


class Categoria(Base):
    __tablename__ = "categorias"
    id_categoria = Column(Integer, primary_key=True, index=True)
    nombre_categoria = Column(String(50), unique=True, nullable=False)
    libros = relationship("Libro", back_populates="categoria")


class Carrito(Base):
    __tablename__ = "carrito"
    id_carrito = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=True)
    id_libro = Column(Integer, ForeignKey("libros.id_libro"), nullable=True)
    cantidad = Column(Integer, default=1)
    fecha_agregado = Column(DateTime, default=datetime.now(timezone.utc))
    usuario = relationship("Usuario", back_populates="carrito")
    libro = relationship("Libro", back_populates="carrito")


class Pedido(Base):
    __tablename__ = "pedidos"
    id_pedido = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=True)
    total = Column(DECIMAL(10, 2), nullable=False)
    fecha_pedido = Column(DateTime, default=datetime.now(timezone.utc))
    estado = Column(String(50), default="Pendiente")
    usuario = relationship("Usuario", back_populates="pedidos")
    detallepedido = relationship(
        "DetallePedido", back_populates="pedido", cascade="all, delete-orphan"
    )


class Valoracion(Base):
    __tablename__ = "valoraciones"
    id_valoracion = Column(Integer, primary_key=True, index=True)
    id_libro = Column(Integer, ForeignKey("libros.id_libro"), nullable=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=True)
    valoracion = Column(Integer, nullable=True)
    fecha_valoracion = Column(DateTime, default=datetime.now(timezone.utc))
    libro = relationship("Libro", back_populates="valoraciones")
    usuario = relationship("Usuario", back_populates="valoraciones")
    __table_args__ = (
        CheckConstraint("valoracion BETWEEN 1 AND 5", name="check_valoracion_range"),
    )


class Tarjeta(Base):
    __tablename__ = "tarjetas"
    id_tarjeta = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=True)
    numero_tarjeta = Column(String(20), nullable=True)
    fecha_expiracion = Column(Date, nullable=True)
    tipo = Column(String(10), nullable=True)
    nombre_titular = Column(String(255), nullable=True)
    usuario = relationship("Usuario", back_populates="tarjetas")


class Registro(Base):
    __tablename__ = "registros"
    id_registro = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=True)
    accion = Column(String(50), nullable=True)
    detalles = Column(Text, nullable=True)
    fecha = Column(DateTime, default=datetime.now(timezone.utc))
    hora = Column(Time, nullable=True)
    usuario = relationship("Usuario", back_populates="registro")


class DetallePedido(Base):
    __tablename__ = "detallepedido"
    id_detallepedido = Column(Integer, primary_key=True, index=True)
    id_pedido = Column(Integer, ForeignKey("pedidos.id_pedido"), nullable=False)
    id_libro = Column(Integer, ForeignKey("libros.id_libro"), nullable=False)
    cantidad = Column(Integer, default=1, nullable=False)
    precio_unitario = Column(DECIMAL(10, 2), nullable=False)
    pedido = relationship("Pedido", back_populates="detallepedido")
    libro = relationship("Libro", back_populates="detallepedido")
