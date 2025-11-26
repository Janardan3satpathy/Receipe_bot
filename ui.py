import streamlit as st
import requests

st.title("🍳 CPU Recipe Bot")
st.write("Trained on 500 datasets. Runs locally.")

ingredients = st.text_input("Enter Ingredients (e.g. Chicken, Rice, Salt):")

if st.button("Find Recipe"):
    if ingredients:
        with st.spinner("Thinking..."):
            try:
                response = requests.post("http://127.0.0.1:8000/generate", json={"ingredients": ingredients})
                if response.status_code == 200:
                    st.success(response.json()["recipe"])
                else:
                    st.error("Error from API")
            except:
                st.error("Is api.py running?")
    else:
        st.warning("Please enter ingredients first.")