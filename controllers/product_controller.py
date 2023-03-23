from sqlalchemy.orm.session import Session
from db.schema import ProductBase, ProductUpdate
from db.models import Products
from fastapi import status, HTTPException




def insert_product(db:Session, request:ProductBase):
    new_product = Products(
        name = request.name,
        category = request.category,
        brand_name = request.brand_name
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {
        "status":status.HTTP_201_CREATED,
        "data":new_product
    }


def update_product(id:int, db:Session, request:ProductUpdate):
    product = db.query(Products).filter(Products.id == id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"Product with id: {id} not found"
        )
    hero_data = request.dict(exclude_unset=True)
    for key, value in hero_data.items():
        setattr(product, key, value)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def delete_product(db:Session, id:int):
    product = db.query(Products).filter(Products.id == id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"Product with id: {id} not found"
        )
    db.delete(product)
    db.commit()
    return {
        "status":status.HTTP_200_OK,
    }
