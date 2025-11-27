import streamlit as st
from transformers import AutoTokenizer, T5ForConditionalGeneration
import torch
import os

# Page Config
st.set_page_config(page_title="AI Recipe Chef", page_icon="🍳")

st.title("🍳 Local AI Recipe Chef")

@st.cache_resource
def load_model():
    local_path = "./my_cpu_model"
    base_model = "google/flan-t5-small"
    
    # 1. Check if folder exists
    if not os.path.exists(local_path):
        st.warning(f"⚠️ Local folder '{local_path}' not found. Using Google base model.")
        return AutoTokenizer.from_pretrained(base_model), T5ForConditionalGeneration.from_pretrained(base_model)

    # 2. Check for LFS Pointers (files that are too small)
    try:
        # Check size of the heavy weights file
        bin_file = os.path.join(local_path, "pytorch_model.bin")
        if os.path.exists(bin_file):
            size_mb = os.path.getsize(bin_file) / (1024 * 1024)
            if size_mb < 10: # If file is less than 10MB, it's likely a Git LFS pointer, not the model
                st.error(f"⚠️ 'pytorch_model.bin' is only {size_mb:.2f} MB. It should be ~300MB.")
                st.info("Falling back to base model because Git LFS upload failed.")
                return AutoTokenizer.from_pretrained(base_model), T5ForConditionalGeneration.from_pretrained(base_model)
    except Exception as e:
        st.warning(f"Could not verify file size: {e}")

    # 3. Try Loading Local Model
    try:
        st.info(f"Attempting to load custom model from {local_path}...")
        tokenizer = AutoTokenizer.from_pretrained(local_path)
        model = T5ForConditionalGeneration.from_pretrained(local_path)
        st.success("✅ Custom local model loaded successfully!")
        return tokenizer, model
    except Exception as e:
        # 4. Fallback if local load fails
        st.error(f"❌ Error loading local model: {e}")
        st.warning("🔄 Falling back to Google's base model so the app still works.")
        return AutoTokenizer.from_pretrained(base_model), T5ForConditionalGeneration.from_pretrained(base_model)

# Load Model
tokenizer, model = load_model()

# Input Area
st.markdown("---")
ingredients = st.text_input("Enter Ingredients (comma separated)", "Chicken, Rice, Salt")

if st.button("Generate Recipe"):
    with st.spinner("Cooking up a recipe..."):
        input_text = f"suggest recipe for: {ingredients}"
        
        # Tokenize
        input_ids = tokenizer(input_text, return_tensors="pt").input_ids
        
        # Generate
        outputs = model.generate(
            input_ids, 
            max_length=200, 
            num_beams=4, 
            early_stopping=True
        )
        
        # Decode
        recipe = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        st.success("Here is your recipe:")
        st.write(recipe)