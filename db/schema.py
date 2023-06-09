from pydantic import BaseModel
from typing import Optional


class ProductBase(BaseModel):
    name: str
    category: str
    brand_name: str
    image_url: str


class ProductDisplay(BaseModel):
    id: int
    name: str
    category: str
    brand_name: str
    image_url: str

    class Config:
        orm_mode = True


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    brand_name: Optional[str] = None
    image_url: Optional[str] = None
