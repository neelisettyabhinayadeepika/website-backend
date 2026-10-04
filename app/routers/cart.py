from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.cart import Cart
from app.schemas.cart_schema import CartCreate


router = APIRouter(prefix="/cart", tags=["Cart"])


# GET ALL CART


@router.get("/")
def get_cart(db: Session = Depends(get_db)):
    return db.query(Cart).all()


# GET SINGLE CART


@router.get("/{id}")
def get_single_cart(id: int, db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.id == id).first()

    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    return cart


# POST CART


@router.post("/")
def create_cart(data: CartCreate, db: Session = Depends(get_db)):
    existing_cart = db.query(Cart).filter(Cart.product_id == data.product_id).first()

    if existing_cart:
        existing_cart.quantity += data.quantity
        db.commit()
        db.refresh(existing_cart)
        return existing_cart

    cart = Cart(product_id=data.product_id, quantity=data.quantity)

    db.add(cart)
    db.commit()
    db.refresh(cart)

    return cart


# UPDATE CART


@router.put("/{id}")
def update_cart(id: int, data: dict, db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.id == id).first()

    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    cart.quantity = data.get("quantity", cart.quantity)

    db.commit()

    db.refresh(cart)

    return cart


# DELETE CART


@router.delete("/{id}")
def delete_cart(id: int, db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.id == id).first()

    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    db.delete(cart)

    db.commit()

    return {"message": "Cart deleted"}
