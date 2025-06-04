from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, DateTime, Date, func
from sqlalchemy.orm import relationship
from .base import BaseModel

class Local(BaseModel):
    __tablename__ = "locales"
    
    nombre = Column(String(255), nullable=False)
    empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=False)
    
    # Relationships
    empresa = relationship("Empresa", back_populates="locales")
    ventas = relationship("Venta", back_populates="local")
    predicciones = relationship("Prediccion", back_populates="local")

class Cliente(BaseModel):
    __tablename__ = "clientes"
    
    nombre = Column(String(255), nullable=False)
    empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=False)
    
    # Relationships
    empresa = relationship("Empresa", back_populates="clientes")
    ventas = relationship("Venta", back_populates="cliente")
    predicciones = relationship("Prediccion", back_populates="cliente")

class Producto(BaseModel):
    __tablename__ = "productos"
    
    nombre = Column(String(255), nullable=False)
    categoria = Column(String(100), nullable=False)
    empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=False)
    
    # Relationships
    empresa = relationship("Empresa", back_populates="productos")
    ventas = relationship("Venta", back_populates="producto")
    predicciones = relationship("Prediccion", back_populates="producto")

class Venta(BaseModel):
    __tablename__ = "ventas"
    
    empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=False)
    local_id = Column(Integer, ForeignKey("locales.id"), nullable=False)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Numeric(12, 2), nullable=False)
    precio_total = Column(Numeric(14, 2), nullable=False)
    timestamp_pedido = Column(DateTime(timezone=True), nullable=False)
    fecha = Column(Date, server_default=func.current_date())
    
    # Relationships
    empresa = relationship("Empresa", back_populates="ventas")
    local = relationship("Local", back_populates="ventas")
    cliente = relationship("Cliente", back_populates="ventas")
    producto = relationship("Producto", back_populates="ventas")

class Prediccion(BaseModel):
    __tablename__ = "predicciones"
    
    empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=False)
    local_id = Column(Integer, ForeignKey("locales.id"), nullable=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=True)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=True)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Numeric(12, 2), nullable=False)
    precio_total = Column(Numeric(14, 2), nullable=False)
    timestamp_pedido = Column(DateTime(timezone=True), nullable=False)
    fecha = Column(Date, server_default=func.current_date())
    
    # Relationships
    empresa = relationship("Empresa", back_populates="predicciones")
    local = relationship("Local", back_populates="predicciones")
    cliente = relationship("Cliente", back_populates="predicciones")
    producto = relationship("Producto", back_populates="predicciones")
