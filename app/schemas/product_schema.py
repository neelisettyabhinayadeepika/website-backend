from pydantic import BaseModel


class ProductSchema(BaseModel):
    title: str
    price: float
    description: str
    image: str
    category: str
