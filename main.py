from fastapi import FastAPI, status
from db import models
from db.db import engine
from routes import products_route

# Initialise a Fast API application
app = FastAPI()


# Root path
@app.get("/")
def home():
    response = {
        "status":status.HTTP_200_OK,
        "data":"Server is running"
    }
    return response

app.include_router(products_route.router)

models.Base.metadata.create_all(engine)