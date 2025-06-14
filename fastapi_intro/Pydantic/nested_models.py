from pydantic import BaseModel


class Address(BaseModel):
    """
    Represents an address with street, city, state, and postal code.
    """
    street: str
    city: str
    state: str
    postal_code: str


class Patient(BaseModel):
    """
    Represents a patient with personal and medical information.
    """
    name: str
    gender: str
    age: int
    address: Address


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

patient1 = Patient(**patient_data)

# Print all values of the patient using the print_patient_details function
print_patient_details(patient1)