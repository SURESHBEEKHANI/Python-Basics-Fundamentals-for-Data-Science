import pydantic
from typing import List, Dict

# Define the 'User' data model with validation using Pydantic
class User(pydantic.BaseModel):
    name: str                # User's name (string)
    age: int                 # User's age (integer)
    weight: float            # User's weight (floating-point number)
    married: bool            # Marital status (boolean)
    allergies: List[str]     # List of allergies (strings)
    contact: Dict[str, str]  # Contact information (dictionary with string keys and values)

# Function that accepts a User instance and prints its attributes and a status message
def display_user_info(user: User) -> None:
    """Displays the user's name, age, and an update message."""
    print(f"Name: {user.name}")
    print(f"Age: {user.age}")
    print(f"married:{user.married}")
    print(f"allergies:{user.allergies}")
    print(f"contact:{user.contact}")
    print("Updating user data...")

# Instantiate a User object with hardcoded values
user1 = User(name="John Doe", age=30, weight=0.0, married=False, allergies=[], contact={})

# Instantiate a User object using data from a dictionary
user_info = {
    "name": "John Doe",
    "age": 30,
    "weight": 70.5,
    "married": True,
    "allergies": ["pollen", "nuts"],
    "contact": {
        "email": "SURESHBEEKHANI26@GMAIL.COM",
        "PHONE": "0340122133"
    }
}
user2 = User(**user_info)

# Call the function with the second User instance
display_user_info(user2)
