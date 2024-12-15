from fastapi import FastAPI

# Create an instance of FastAPI
app = FastAPI()

# Define a simple route
@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}

# Define another route with a path parameter
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "query": q}

# Define a route with a POST method
@app.post("/items/")
def create_item(item: dict):
    return {"message": "Item created successfully!", "item": item}
