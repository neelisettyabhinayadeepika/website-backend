from sqlalchemy import Column, Integer, String, Float,JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String)
    image = Column(String)
    category = Column(String)


    carts = relationship("Cart", back_populates="product")