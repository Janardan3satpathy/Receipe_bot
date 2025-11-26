import streamlit as st
from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch
import os

# --- Page Config ---
st.set_page_config(page_title="My Recipe AI", page_icon="🍳")

# --- Model Loading (Cached) ---
# We use @st.cache_resource so the model loads only once, not every time you click a button.
@st.cache_resource
def load_model():
    # Try to load the local model (if uploaded to GitHub)
    local_path = "./my_cpu_model"
    
    if os.path.exists(local_path):
        status_text.text("Loading your custom fine-tuned model...")
        tokenizer = T5Tokenizer.from_pretrained(local_path)
        model = T5ForConditionalGeneration.from_pretrained(local_path)
    else:
        # Fallback to the base model if local files are missing (Safety net for GitHub)
        status_text.text("Custom model not found. Loading base Google model...")
        model_name = "google/flan-t5-small"
        tokenizer = T5Tokenizer.from_pretrained(model_name)
        model = T5ForConditionalGeneration.from_pretrained(model_name)
    
    return tokenizer, model

# --- UI Layout ---
st.title("🍳 AI Recipe Generator")
st.markdown("This app runs entirely on the cloud using **Streamlit**.")

# Placeholder for status messages
status_text = st.empty()

# Load the model
with st.spinner("Waking up the AI chef..."):
    try:
        tokenizer, model = load_model()
        status_text.empty() # Clear message once loaded
    except Exception as e:
        st.error(f"Error loading model: {e}")
        st.stop()

# Input Area
ingredients = st.text_input("Enter Ingredients (e.g. Chicken, Rice, Salt):")

if st.button("Generate Recipe"):
    if ingredients:
        input_text = f"suggest recipe for: {ingredients}"
        
        # Run Inference
        with st.spinner("Cooking..."):
            input_ids = tokenizer(input_text, return_tensors="pt").input_ids
            outputs = model.generate(input_ids, max_length=150)
            recipe = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Display Result
        st.success("Here is your recipe:")
        st.write(recipe)
    else:
        st.warning("Please enter some ingredients first.")