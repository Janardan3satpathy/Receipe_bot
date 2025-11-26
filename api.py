from fastapi import FastAPI
from pydantic import BaseModel
from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch

app = FastAPI()
MODEL_DIR = "./my_cpu_model"

print("⏳ Loading your trained model...")
try:
    tokenizer = T5Tokenizer.from_pretrained(MODEL_DIR)
    model = T5ForConditionalGeneration.from_pretrained(MODEL_DIR)
    print("✅ Model loaded successfully!")
except:
    print("⚠️ Model not found. Please run train.py first.")

class Query(BaseModel):
    ingredients: str

@app.post("/generate")
def generate(query: Query):
    input_text = f"suggest recipe for: {query.ingredients}"
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids
    
    # Generate response
    outputs = model.generate(input_ids, max_length=100)
    recipe = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return {"recipe": recipe}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)