import streamlit as st
import requests

# Title of the app
st.title("SHL Assessment Recommender")

# Input form
query = st.text_input("Enter your query to get recommendations:")

if query:
    # Call the FastAPI endpoint (adjust URL if needed)
    response = requests.post("http://localhost:8000/recommend", json={"query": query})

    if response.status_code == 200:
        # Show the results
        recommendations = response.json().get("recommended_assessments", [])
        for rec in recommendations:
            st.write(f"**Description**: {rec['description']}")
            st.write(f"**Duration**: {rec['duration']} minutes")
            st.write(f"**Remote Support**: {rec['remote_support']}")
            st.write(f"**Test Type**: {', '.join(rec['test_type'])}")
            st.write(f"[Link to Assessment]({rec['url']})")
            st.write("---")
    else:
        st.error("Error: Unable to fetch recommendations.")
