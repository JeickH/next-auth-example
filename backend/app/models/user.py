from sqlalchemy import Column, String, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .base import BaseModel, Base
import enum

class UserPlan(str, enum.Enum):
    FREE = "free"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"

class User(BaseModel):
    __tablename__ = "users"
    
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    document = Column(String(50), unique=True, nullable=False)
    document_type = Column(String(20), nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    plan = Column(Enum(UserPlan), default=UserPlan.FREE, nullable=False)
    
    # Relationships
    empresa = relationship("Empresa", back_populates="users", uselist=False)

class Empresa(BaseModel):
    __tablename__ = "empresas"
    
    nombre = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    users = relationship("User", back_populates="empresa")
    locales = relationship("Local", back_populates="empresa")
    clientes = relationship("Cliente", back_populates="empresa")
    productos = relationship("Producto", back_populates="empresa")
    ventas = relationship("Venta", back_populates="empresa")
    predicciones = relationship("Prediccion", back_populates="empresa")
