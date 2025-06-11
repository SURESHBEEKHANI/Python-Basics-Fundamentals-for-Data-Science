import streamlit as st
import requests

# Set the FastAPI base URL
BASE_URL = "http://127.0.0.1:8000"

# Streamlit app title
st.title("Patient Management System")

# Navigation menu
menu = ["Home", "View All Patients", "View Patient", "Sort Patients", "Create Patient", "Update Patient", "Delete Patient"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Home":
    st.subheader("Welcome to the Patient Management System")
    st.write("This system allows you to manage patient data, view details, and perform various operations.")

elif choice == "View All Patients":
    st.subheader("View All Patients")
    response = requests.get(f"{BASE_URL}/view")
    if response.status_code == 200:
        patients = response.json()
        st.json(patients)
    else:
        st.error("Failed to fetch patient data.")

elif choice == "View Patient":
    st.subheader("View Patient by ID")
    patient_id = st.text_input("Enter Patient ID", "")
    if st.button("View Patient"):
        response = requests.get(f"{BASE_URL}/patient/{patient_id}")
        if response.status_code == 200:
            patient = response.json()
            st.json(patient)
        else:
            st.error("Patient not found.")

elif choice == "Sort Patients":
    st.subheader("Sort Patients")
    sort_by = st.selectbox("Sort By", ["height", "weight", "bmi"])
    order = st.radio("Order", ["asc", "desc"])
    if st.button("Sort"):
        response = requests.get(f"{BASE_URL}/sort", params={"sort_by": sort_by, "order": order})
        if response.status_code == 200:
            sorted_patients = response.json()
            st.json(sorted_patients)
        else:
            st.error("Failed to sort patients.")

elif choice == "Create Patient":
    st.subheader("Create New Patient")
    patient_id = st.text_input("Patient ID")
    name = st.text_input("Name")
    city = st.text_input("City")
    age = st.number_input("Age", min_value=1, max_value=119, step=1)
    gender = st.selectbox("Gender", ["male", "female", "others"])
    height = st.number_input("Height (in meters)", min_value=0.1, step=0.01)
    weight = st.number_input("Weight (in kg)", min_value=0.1, step=0.1)

    if st.button("Create Patient"):
        patient_data = {
            "id": patient_id,
            "name": name,
            "city": city,
            "age": age,
            "gender": gender,
            "height": height,
            "weight": weight
        }
        response = requests.post(f"{BASE_URL}/create", json=patient_data)
        if response.status_code == 201:
            st.success("Patient created successfully.")
        else:
            st.error("Failed to create patient.")

elif choice == "Update Patient":
    st.subheader("Update Patient")
    patient_id = st.text_input("Enter Patient ID to Update")
    name = st.text_input("Name (optional)")
    city = st.text_input("City (optional)")
    age = st.number_input("Age (optional)", min_value=1, max_value=119, step=1, value=0)
    gender = st.selectbox("Gender (optional)", ["", "male", "female", "others"])
    height = st.number_input("Height (optional, in meters)", min_value=0.0, step=0.01, value=0.0)
    weight = st.number_input("Weight (optional, in kg)", min_value=0.0, step=0.1, value=0.0)

    if st.button("Update Patient"):
        update_data = {}
        if name:
            update_data["name"] = name
        if city:
            update_data["city"] = city
        if age > 0:
            update_data["age"] = age
        if gender:
            update_data["gender"] = gender
        if height > 0:
            update_data["height"] = height
        if weight > 0:
            update_data["weight"] = weight

        response = requests.put(f"{BASE_URL}/edit/{patient_id}", json=update_data)
        if response.status_code == 200:
            st.success("Patient updated successfully.")
        else:
            st.error("Failed to update patient.")

elif choice == "Delete Patient":
    st.subheader("Delete Patient")
    patient_id = st.text_input("Enter Patient ID to Delete")
    if st.button("Delete Patient"):
        response = requests.delete(f"{BASE_URL}/delete/{patient_id}")
        if response.status_code == 200:
            st.success("Patient deleted successfully.")
        else:
            st.error("Failed to delete patient.")
