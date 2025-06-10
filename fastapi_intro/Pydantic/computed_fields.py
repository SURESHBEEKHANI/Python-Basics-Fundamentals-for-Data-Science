# Import necessary modules from Pydantic and typing
from pydantic import BaseModel, EmailStr, AnyUrl, computed_field
from typing import List, Dict, Optional


# Define the User model with various fields and a computed BMI property
class User(BaseModel):
    name: str  # Full name of the user
    age: int  # User's age
    email: EmailStr  # Validated email address
    linkedin: AnyUrl  # Validated LinkedIn URL
    weight: float  # User's weight in kilograms
    height: float  # User's height in meters
    married: Optional[bool] = None  # Optional marital status
    allergies: Optional[List[str]] = None  # Optional list of allergies
    contact: Dict[str, str]  # Dictionary of contact details (e.g., phone, emergency)

    @computed_field
    @property
    def calaculate_bmi(self) -> float:
        """
        Calculates the Body Mass Index (BMI) based on weight and height.
        BMI = weight (kg) / (height (m))^2
        """
        bmi = round(self.weight / (self.height ** 2), 2)
        return bmi


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
    print(f"Height: {user.height}")
    print(f"BMI: {user.calaculate_bmi}")
    print(f"Married: {user.married}")
    print(f"Allergies: {user.allergies}")
    print(f"Contact Info: {user.contact}")


# Example usage: Creating a User instance from a dictionary
user_data = {
    "name": "Jane Smith",
    "age": 39,  # User's age
    "email": "janeex@hdfc.com",  # Valid email
    "linkedin": "https://www.linkedin.com/in/janesmith",
    "weight": 25.0,  # User's weight in kg
    "height": 1.75,  # User's height in meters
    "married": None,
    "contact": {
        "phone": "987-654-3210",
        "emergency": "123-456-7890"  # Emergency contact
    }
}

# Create User object and print details
user_instance = User(**user_data)
print_user_details(user_instance)
