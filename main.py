from fastapi import FastAPI, status
from db import models
from db.db import engine
from routes import products_route
from fastapi.middleware.cors import CORSMiddleware

# Initialise a Fast API application
app = FastAPI()


# Root path
@app.get("/")
def home():
    response = {
        "status": status.HTTP_200_OK,
        "data": "Server is running"
    }
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


app.include_router(products_route.router)

models.Base.metadata.create_all(engine)
