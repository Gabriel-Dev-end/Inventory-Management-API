from fastapi import FastAPI
from pydantic import BaseModel
from models import Product
import json
import os

app = FastAPI()
estoque = []
db_file = "database.json"

def save_data():
    saver = []
    for item in estoque:
        saver.append(item.model_dump())
    with open(db_file,"w") as f:
        json.dump(saver, f, indent=4)

def load_data():
    if not os.path.exists(db_file):
        return []
    with open(db_file,"r") as db:
        brute_db = json.load(db)
        loader = []
        for item in brute_db:
            product_object = Product(**item)
            loader.append(product_object)
        return loader


@app.post("/products/")
def create_product(Product: Product):
    Product.id = len(estoque) + 1
    estoque.append(Product)
    save_data()
    return Product

@app.get("/products/{id}")
def list_products(id:int):
    for item in estoque:
        if item.id == id:
            return item
    return {"message": "Product not found"}

@app.delete("/products/{id}")
def delete_product(id:int):
    for item in estoque:
        if item.id == id:
            estoque.remove(item)
            save_data()
            return None
    return {"message": "Product not found"}

@app.put("/products/{id}")
def edit_product(id:int,new_item:Product):
    for item in estoque:
        if item.id == id:
            item.name = new_item.name
            item.price = new_item.price
            item.quantity = new_item.quantity
            save_data()
            return new_item
    return {"message": "Product not found"}