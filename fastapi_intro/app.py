# Import FastAPI class from fastapi package
from fastapi import FastAPI

# Create FastAPI app instance with metadata
app = FastAPI(
    title="FastAPI UV Project",  # Title of the API
    description="A FastAPI project managed with uv",  # Description of the API
    version="1.0.0"  # Version of the API
)

# Root endpoint: returns a welcome message
@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI with uv!"}

# Endpoint 1: Greets the user by name
@app.get("/hello/{name}")
def greet_user(name: str):
    return {"message": f"Hello, {name}!"}

# Endpoint 2: Returns the square of a given number
@app.get("/square/{number}")
def square_number(number: int):
    return {"number": number, "square": number * number}
