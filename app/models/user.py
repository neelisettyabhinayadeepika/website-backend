from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)

    email = Column(String, unique=True, index=True)

    role = Column(String, default="user")

    password = Column(String)

    carts = relationship("Cart", back_populates="user")
    tasks = relationship("Task", back_populates="user")
