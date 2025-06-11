import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000" 

st.title("Insurance Premium Category Predictor")
st.markdown("Enter your details below:")

# Input fields
age = st.number_input("Age", min_value=1, max_value=119, value=30)
weight = st.number_input("Weight (kg)", min_value=1.0, value=65.0)
height = st.number_input("Height (m)", min_value=0.5, max_value=2.5, value=1.7)
income_lpa = st.number_input("Annual Income (LPA)", min_value=0.1, value=10.0)
smoker = st.selectbox("Are you a smoker?", options=[True, False])
city = st.text_input("City", value="Mumbai")
occupation = st.selectbox(
    "Occupation",
    ['retired', 'freelancer', 'student', 'government_job', 'business_owner', 'unemployed', 'private_job']
)

if st.button("Predict Premium Category"):
    input_data = {
        "age": age,
        "weight": weight,
        "height": height,
        "income_lpa": income_lpa,
        "smoker": smoker,
        "city": city,
        "occupation": occupation
    }

    try:
        response = requests.post(API_URL + "/predict", json=input_data, timeout=10)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)

        result = response.json()
        if "predicted_category" in result:
            st.success(f"Predicted Insurance Premium Category: **{result['predicted_category']}**")
        else:
            st.error("Unexpected response format from the API.")
            st.json(result)

    except requests.exceptions.ConnectionError:
        st.error("❌ Could not connect to the FastAPI server. Please ensure it is running.")
    except requests.exceptions.Timeout:
        st.error("⏳ The request timed out. Please try again later.")
    except requests.exceptions.RequestException as e:
        st.error(f"⚠️ An error occurred: {e}")
