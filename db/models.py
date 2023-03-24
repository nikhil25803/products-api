from sqlalchemy import  Column, String, Integer,LargeBinary
from db.db import Base


class Products(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    category = Column(String)
    brand_name = Column(String)
    image_url = Column(String)