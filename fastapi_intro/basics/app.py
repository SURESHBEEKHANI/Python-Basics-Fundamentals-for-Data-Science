# Import FastAPI class from fastapi package
from fastapi import FastAPI
import uvicorn
# Create FastAPI app instance with metadata
app = FastAPI(
    title="FastAPI",  # Title of the API
    description="A FastAPI project managed with uv",  # Description of the API
    version="1.0.0"  # Version of the API
)

# Root endpoint: returns a welcome message
@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI with uv!"}

# Endpoint 1: Greets the user by name
@app.get("/hello")
def greet_user(name: str):
    return {"message": f"Hello, {name}!"}

# Endpoint 2: Returns the square of a given number
@app.get("/square/{number}")
def square_number(number: int):
    return {"number": number, "square": number * number}


# Endpoint to get the length of the text
if __name__ == "__main__":

    # Run the FastAPI app using uvicorn server
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)