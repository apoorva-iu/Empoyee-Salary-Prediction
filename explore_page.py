import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ----------- Helpers -----------

def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = "Other"
    return categorical_map

def clean_experience(x):
    if x == "More than 50 years":
        return 50
    if x == "Less than 1 year":
        return 0.5
    return float(x)

def clean_education(x):
    if "Bachelor’s degree" in x:
        return "Bachelor’s degree"
    if "Master’s degree" in x:
        return "Master’s degree"
    if "Professional degree" in x or "Other doctoral" in x:
        return "Post grad"
    return "Less than a Bachelors"

# ----------- Load Data -----------

@st.cache_data
def load_df():
    data = pd.read_csv(r"C:\Users\Admin\Documents\Employee_salary_prediction\survey_results_public.csv")
    data = data[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedComp"]]
    data = data[data["ConvertedComp"].notnull()]
    data = data.dropna()
    data = data[data["Employment"] == "Employed full-time"]
    data = data.drop("Employment", axis=1)

    country_map = shorten_categories(data["Country"].value_counts(), 400)
    data["Country"] = data["Country"].map(country_map)

    data = data[data["ConvertedComp"] <= 250000]
    data = data[data["ConvertedComp"] >= 10000]
    data = data[data["Country"] != "Other"]

    data["YearsCodePro"] = data["YearsCodePro"].apply(clean_experience)
    data["EdLevel"] = data["EdLevel"].apply(clean_education)
    data = data.rename({"ConvertedComp": "Salary"}, axis=1)
    return data

# ----------- Page -----------

def show_explore_page(data):
    st.title("Explore Software Engineer Salaries")
    st.write("### Based on Stack Overflow Developer Survey 2020")

    # ---- Country Pie Chart ----
    st.subheader("🌍 Number of Data from Different Countries")
    country_counts = data["Country"].value_counts()

    fig1, ax1 = plt.subplots()
    ax1.pie(
        country_counts.values,
        labels=country_counts.index,
        autopct="%1.1f%%",
        shadow=True,
        startangle=90,
    )
    ax1.axis("equal")
    st.pyplot(fig1, use_container_width=True)

    # ---- Mean Salary by Country ----
    st.subheader("💰 Mean Salary Based on Country")
    mean_salary_country = data.groupby("Country")["Salary"].mean().sort_values()
    st.bar_chart(mean_salary_country, use_container_width=True)

    # ---- Mean Salary by Experience ----
    st.subheader("📈 Mean Salary Based on Years of Experience")
    mean_salary_experience = data.groupby("YearsCodePro")["Salary"].mean().sort_index()
    st.line_chart(mean_salary_experience, use_container_width=True)
