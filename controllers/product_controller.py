from sqlalchemy.orm.session import Session
from typing import Optional
from db.schema import ProductBase, ProductUpdate
from db.models import Products
from fastapi import status, HTTPException, File, Query
from dotenv import load_dotenv
import os
import datetime
import boto3

load_dotenv()


AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.environ.get("AWS_REGION")
S3_Bucket = os.environ.get("S3_Bucket")
S3_Key = os.environ.get("S3_Key")

aws_session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)
s3_client = aws_session.client("s3")


def insert_product(db: Session, request):

    file_received: File = request["image_data"]

    filename = file_received.filename
    current_time = datetime.datetime.now()
    split_file_name = os.path.splitext(filename)
    s3_file_name = str(current_time.timestamp()).replace('.', '')
    file_extension = split_file_name[1]
    data = file_received.file._file

    s3_upload = s3_client.put_object(
        Bucket=S3_Bucket,
        Body=data,
        Key=S3_Key + s3_file_name + file_extension
    )

    if s3_upload:
        s3_url = f"https://{S3_Bucket}.s3.{AWS_REGION}.amazonaws.com/{S3_Key}{s3_file_name +  file_extension}"
    else:
        raise HTTPException(status_code=400, detail="Failed to upload in S3")
    new_product = Products(
        name=request["name"],
        category=request["category"],
        brand_name=request["brand_name"],
        image_url=s3_url
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


def get_products(db: Session, search=None):
    if search != None:
        products = db.query(Products).filter(
            Products.name.contains(search)).all()
    else:
        products = db.query(Products).all()
    return products


def update_product(id: int, db: Session, request: ProductUpdate):
    product = db.query(Products).filter(Products.id == id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id: {id} not found"
        )
    hero_data = request.dict(exclude_unset=True)
    for key, value in hero_data.items():
        setattr(product, key, value)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, id: int):
    product = db.query(Products).filter(Products.id == id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id: {id} not found"
        )
    db.delete(product)
    db.commit()
    return {
        "status": status.HTTP_200_OK,
    }
