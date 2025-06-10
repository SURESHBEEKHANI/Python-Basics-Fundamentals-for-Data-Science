# Import necessary modules from Pydantic and typing
from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator
from typing import List, Dict, Optional

class User(BaseModel):
    """
    Represents a user with personal and contact information.
    Uses Pydantic's Field for validation and metadata.
    """
    name: str = Field(..., min_length=1, max_length=50, title="User Name", description="The full name of the user")  # User's name with length constraints
    age: int = Field(..., gt=0, lt=120, description="Age must be between 1 and 119")  # User's age with range validation
    email: EmailStr  # Validated email address
    linkedin: AnyUrl  # Validated LinkedIn URL
    weight: float = Field(..., gt=0, description="Weight must be greater than 0")  # User's weight, must be positive
    married: Optional[bool] = Field(None, title="Marital Status", description="Indicates if the user is married or not")  # Optional marital status
    allergies: Optional[List[str]] = None  # Optional list of allergies
    contact: Dict[str, str]  # Dictionary of contact details (e.g., phone)

# Function to print all details of a User instance
def print_user_details(user: User) -> None:
    """
    Prints the details of a User instance.
    """
    print(f"Name: {user.name}")
    print(f"Age: {user.age}")
    print(f"Email: {user.email}")
    print(f"LinkedIn: {user.linkedin}")
    print(f"Weight: {user.weight}")
    print(f"Married: {user.married}")
    print(f"Allergies: {user.allergies}")
    print(f"Contact Info: {user.contact}")

# Example usage: Creating a User from a dictionary
user_data = {
    "name": "Jane Smith",
    "age": -28,  # Invalid age (should trigger validation error)
    "email": "janeex@mple.com",  # Invalid email domain (should trigger validation error)
    "linkedin": "https://www.linkedin.com/in/janesmith",
    "weight": 65.0,
    "contact": {
        "phone": "987-654-3210"
    }
}

user_instance = User(**user_data)
print_user_details(user_instance)
