from fastapi import FastAPI , HTTPException
from pydantic import BaseModel
from typing import List, Dict,Optional
import uvicorn


# Import FastAPI class from fastapi package
# Create FastAPI app instance with metadata
app = FastAPI(
    title="Text Processing API",
    description="API for processing text with various operations",
    version="1.0.0"
)


# define pydantic models for request and response pameters
class TextRequest(BaseModel):
    text: str
    uppercase: Optional[bool] = False

class TextResponse(BaseModel):
    processed: str
    length: int

@app.get("/")
def read_root():
    return {"message": "Welcome to the Text Processing API!"}

# define a route endpoint for processing text
@app.post("/process_text", response_model=TextResponse)
# Process the input text based on the request parameters
# return processed text and its length
def process_text(request: TextRequest):
    """
    Process the input text based on the request parameters.
    If uppercase is True, convert text to uppercase.
    Return processed text and its length.
    """
    text= request.text
    # Check if the text is empty
    # If text is empty, raise an HTTP exception with status code 400
    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    # Process the text based on the request parameters
    # If uppercase is True, convert text to uppercase
    processed_text = text.upper() if request.uppercase else text
    
    return TextResponse(processed=processed_text, length=len(processed_text))

# Endpoint to get the length of the text
if __name__ == "__main__":

    # Run the FastAPI app using uvicorn server
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)