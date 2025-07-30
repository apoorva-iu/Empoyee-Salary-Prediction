# predict_page.py
import streamlit as st
import pickle
import numpy as np

# -------- Model / encoders loader (cached) --------
@st.cache_resource
def load_artifacts():
    with open("saved_steps.pkl", "rb") as file:
        data = pickle.load(file)
    # Expecting keys: "model", "le_country", "le_education"
    return data["model"], data["le_country"], data["le_education"]

regressor, le_country, le_education = load_artifacts()

# -------- Page --------
def show_predict_page():
    st.title("Employee Salary Prediction")
    st.subheader("Calculate Your Salary")

    # Use the label encoder classes as the dropdown options
    countries = list(le_country.classes_)
    education_levels = list(le_education.classes_)

    # Unique keys to avoid duplicate element IDs
    country = st.selectbox("🌍 Country", countries, key="predict_country")
    education = st.selectbox("🎓 Education Level", education_levels, key="predict_education")
    experience = st.slider("💼 Years of Experience", 0, 50, 1, key="predict_experience")

    if st.button("Calculate Salary 💰", key="predict_button"):
        try:
            # Build feature array from user inputs
            X = np.array([[country, education, experience]], dtype=object)

            # Transform categorical columns using your encoders
            X[:, 0] = le_country.transform(X[:, 0])
            X[:, 1] = le_education.transform(X[:, 1])

            # Ensure numeric dtype for the model
            X = X.astype(float)

            # Predict
            salary = regressor.predict(X)
            st.subheader(f"💵 Estimated Salary: ${salary[0]:,.2f}")
        except Exception as e:
            st.error("Oops! Something went wrong while predicting.")
            st.exception(e)
