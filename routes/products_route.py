from fastapi import APIRouter, File
from fastapi import Depends
from db.schema import ProductBase, ProductDisplay, ProductUpdate
from sqlalchemy.orm.session import Session
from db.db import get_db
from controllers import product_controller
from fastapi import UploadFile, Form

router = APIRouter(prefix="/products", tags=["product"])


@router.post('/')
async def insert_product(
    db: Session = Depends(get_db),
    name: str = Form(...),
    category: str = Form(...),
    brand_name: str = Form(...),
    image : UploadFile = File(...)
):
    

    request = {
        "name": name,
        "category": category,
        "brand_name": brand_name,
        "image_data": image
    }

    return product_controller.insert_product(db, request)


@router.put('/{id}', response_model=ProductDisplay)
def update_product(id: int, request: ProductUpdate, db: Session = Depends(get_db)):

    return product_controller.update_product(id=id, db=db, request=request)


@router.delete("/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):

    return product_controller.delete_product(db=db, id=id)
