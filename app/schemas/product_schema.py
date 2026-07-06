from pydantic import BaseModel
from typing import List


class ProductSchema(BaseModel):
    title: str
    price: float
    description: str
    image: str
    category: str

  