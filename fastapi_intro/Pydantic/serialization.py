# Import BaseModel from Pydantic for data validation and serialization
from pydantic import BaseModel


# Define Address model for nested serialization
class Address(BaseModel):
    """
    Represents an address with street, city, state, and postal code.
    """
    street: str
    city: str
    state: str
    postal_code: str


# Define Patient model with nested Address
class Patient(BaseModel):
    """
    Represents a patient with personal and medical information.
    """
    name: str
    gender: str
    age: int
    address: Address


# Function to print all details of a Patient instance, including nested address
def print_patient_details(patient: Patient) -> None:
    """
    Prints the details of a Patient instance, including nested address.
    """
    print(f"Name: {patient.name}")
    print(f"Gender: {patient.gender}")
    print(f"Age: {patient.age}")
    print("Address:")
    print(f"  Street: {patient.address.street}")
    print(f"  City: {patient.address.city}")
    print(f"  State: {patient.address.state}")
    print(f"  Postal Code: {patient.address.postal_code}")


# Example usage: Creating Address and Patient instances from dictionaries
address_data = {
    "street": "123 Main St",
    "city": "Springfield",
    "state": "IL",
    "postal_code": "62701"
}

patient_data = {
    "name": "John Doe",
    "gender": "male",
    "age": 30,
    "address": address_data
}

# Create Patient instance from dictionary
patient1 = Patient(**patient_data)

# Demonstrate Pydantic serialization methods
# model_dump returns a dict representation of the model
# model_dump_json returns a JSON string, with options to include/exclude fields
# exclude_unset only includes fields that were set
temp = patient1.model_dump  # Reference to the model_dump method (not called)
temp2 = patient1.model_dump_json(exclude=["name", "age"])  # JSON without name and age
temp3 = patient1.model_dump_json(include=["name", "age"])  # JSON with only name and age
temp4 = patient1.model_dump_json(exclude_unset=True)  # JSON with only set fields

# Print the various serialization outputs
print(temp2)
print(temp3)
print(temp4)
print(temp)  # This will print the method object, not the data
print(type(temp))
print(type(temp2))