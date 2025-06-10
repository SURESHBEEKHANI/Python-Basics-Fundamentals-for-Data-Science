# Import necessary modules from Pydantic and typing
from pydantic import BaseModel, EmailStr, AnyUrl, model_validator
from typing import List, Dict, Optional


# Define the User model with various fields and a model-level validator
class User(BaseModel):
    name: str  # Full name of the user
    age: int  # User's age
    email: EmailStr  # Validated email address
    linkedin: AnyUrl  # Validated LinkedIn URL
    weight: float  # User's weight
    married: Optional[bool] = None  # Optional marital status
    allergies: Optional[List[str]] = None  # Optional list of allergies
    contact: Dict[str, str]  # Dictionary of contact details (e.g., phone, emergency)

    @model_validator(mode='after')
    @classmethod
    def validate_emergency_contact(cls, model):
        """
        Ensures that users over 60 years of age have an emergency contact listed.
        """
        if model.age > 60 and 'emergency' not in model.contact:
            raise ValueError("Emergency contact is required for users over 60")
        return model


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


# Example usage: Creating a User instance from a dictionary
user_data = {
    "name": "Jane Smith",
    "age": 39,  # User's age
    "email": "janeex@hdfc.com",  # Valid email
    "linkedin": "https://www.linkedin.com/in/janesmith",
    "weight": 25.0,
    "married": None,
    "contact": {
        "phone": "987-654-3210",
        "emergency": "123-456-7890"  # Emergency contact
    }
}

# Create User object and print details
user_instance = User(**user_data)
print_user_details(user_instance)
