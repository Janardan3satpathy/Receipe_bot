import json
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, T5ForConditionalGeneration
from torch.optim import AdamW  # <--- CHANGED: Import from torch.optim instead of transformers

# Config
MODEL_NAME = "google/flan-t5-small"
OUTPUT_DIR = "./my_cpu_model"
EPOCHS = 3
BATCH_SIZE = 4  # Small batch size for CPU

class RecipeDataset(Dataset):
    def __init__(self, data, tokenizer, max_len=128):
        self.data = data
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        item = self.data[index]
        input_text = f"suggest recipe for: {item['ingredients']}"
        target_text = item['recipe']

        input_enc = self.tokenizer(input_text, max_length=self.max_len, padding="max_length", truncation=True, return_tensors="pt")
        target_enc = self.tokenizer(target_text, max_length=self.max_len, padding="max_length", truncation=True, return_tensors="pt")

        return {
            "input_ids": input_enc.input_ids.flatten(),
            "attention_mask": input_enc.attention_mask.flatten(),
            "labels": target_enc.input_ids.flatten()
        }

def train():
    print("⏳ Loading model and tokenizer...")
    # Use AutoTokenizer to avoid 'sentencepiece' dependency issues
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME)
    
    # Force CPU usage
    device = torch.device("cpu")
    model.to(device)
    
    print("📂 Loading 500 dataset entries...")
    try:
        with open("recipes_500.json", "r") as f:
            raw_data = json.load(f)
    except FileNotFoundError:
        print("❌ Error: recipes_500.json not found. Run data_gen.py first!")
        return

    dataset = RecipeDataset(raw_data, tokenizer)
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)
    
    # Initialize Optimizer
    optimizer = AdamW(model.parameters(), lr=1e-4)

    print("🚀 Starting Training on CPU (This will take a few minutes)...")
    model.train()
    
    for epoch in range(EPOCHS):
        total_loss = 0
        for step, batch in enumerate(dataloader):
            optimizer.zero_grad()
            
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["labels"].to(device)
            
            outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
            loss = outputs.loss
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            
            # Print progress every 20 batches
            if step % 20 == 0:
                print(f"  Epoch {epoch+1}, Step {step}/{len(dataloader)} - Loss: {loss.item():.4f}")
        
        print(f"✅ Epoch {epoch+1} Complete. Avg Loss: {total_loss/len(dataloader):.4f}")

    print("💾 Saving model...")
    # safe_serialization=False ensures it saves as 'pytorch_model.bin' to match your git lfs track "*.bin"
    model.save_pretrained(OUTPUT_DIR, safe_serialization=False)
    tokenizer.save_pretrained(OUTPUT_DIR)
    print(f"🎉 Model saved to {OUTPUT_DIR}")

if __name__ == "__main__":
    train()