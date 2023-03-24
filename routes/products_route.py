from fastapi import APIRouter
from fastapi import Depends, File, UploadFile
from db.schema import ProductBase, ProductDisplay, ProductUpdate
from sqlalchemy.orm.session import Session
from db.db import get_db
from controllers import product_controller

router = APIRouter(prefix="/products", tags=["product"])


@router.post('/')
async def insert_product(request: ProductBase,files: UploadFile = File(...), db: Session = Depends(get_db)):
    print(files.filename)

    return product_controller.insert_product(db, request)


@router.put('/{id}', response_model=ProductDisplay)
def update_product(id: int, request: ProductUpdate, db: Session = Depends(get_db)):

    return product_controller.update_product(id=id, db=db, request=request)


@router.delete("/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):

    return product_controller.delete_product(db=db, id=id)
