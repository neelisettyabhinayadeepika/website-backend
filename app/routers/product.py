from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.product import Product
from app.schemas.product_schema import ProductSchema
from app.core.auth import role_required

router = APIRouter(prefix="/products", tags=["Products"])


# GET ALL PRODUCTS
@router.get("/")
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


# GET SINGLE PRODUCT
@router.get("/{id}")
def get_product(id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


# CREATE PRODUCT
@router.post("/")
def create_product(
    product: ProductSchema,
    db: Session = Depends(get_db),
    current_user=Depends(role_required(["superadmin"])),
):
    new_product = Product(
        title=product.title,
        price=product.price,
        description=product.description,
        image=product.image,
        category=product.category,
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


# UPDATE PRODUCT
@router.put("/{id}")
def update_product(
    id: int,
    product: ProductSchema,
    db: Session = Depends(get_db),
    current_user=Depends(role_required(["superadmin"])),
):
    db_product = db.query(Product).filter(Product.id == id).first()

    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    db_product.title = product.title
    db_product.price = product.price
    db_product.description = product.description
    db_product.image = product.image
    db_product.category = product.category

    db.commit()
    db.refresh(db_product)

    return db_product


# DELETE PRODUCT (SUPER ADMIN ONLY)
@router.delete("/{id}")
def delete_product(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(role_required(["superadmin"])),
):
    db_product = db.query(Product).filter(Product.id == id).first()

    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(db_product)
    db.commit()

    return {"message": "Product deleted successfully"}
