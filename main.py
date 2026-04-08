from fastapi import FastAPI
from pydantic import BaseModel
from models import Product
app = FastAPI()
estoque = []

@app.post("/products/")
def create_product(Product: Product):
