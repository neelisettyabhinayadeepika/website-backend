from pydantic import BaseModel
from typing import Optional


class CartCreate(BaseModel):
    product_id: int
    quantity: int = 1


class CartUpdate(BaseModel):
    quantity: Optional[int] = None
