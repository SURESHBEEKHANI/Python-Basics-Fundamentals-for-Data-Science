from pydantic import BaseModel, EmailStr, AnyUrl, Field,field_validator

from typing import List, Dict, Optional

class User(BaseModel):
    name: str 
    age: int 
    email: EmailStr
    linkedin: AnyUrl
    weight: float 
    married: Optional[bool] = None  # Set default to None to make it optional
    allergies: Optional[List[str]] = None
    contact: Dict[str, str]


    @field_validator('email')
    @classmethod
    def validate_email(cls, value):
      valid_domains = ['hdfc.com', 'icici.com']
      domains_name = value.split('@')[-1]
      if domains_name not in valid_domains:
          raise ValueError(f"not a valid email domain: {domains_name}. Allowed domains are: {', '.join(valid_domains)}")
      return value
    
    @field_validator('name')
    @classmethod
    def tramsform_name(cls, value):
        """
        Transforms the name to title case.
        """
        return value.upper()
    
    @field_validator('age', mode='after')
    @classmethod
    def validate_age(cls, value):
        """
        Validates that age is between 1 and 119.
        """
        if not (0<= value <= 119):
            raise ValueError("Age must be between 1 and 119")
        return value

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
    "age":"28",  # Ensure age is a valid integer
    "email": "janeex@hdfc.com",  # Use a valid domain for email
    "linkedin": "https://www.linkedin.com/in/janesmith",
    "weight": 65.0,
    "married": None,  # Add this field to avoid missing error
    "contact": {
        "phone": "987-654-3210"
    }
}

user_instance = User(**user_data)
print_user_details(user_instance)