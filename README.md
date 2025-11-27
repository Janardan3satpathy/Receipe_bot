# **🍳 Local AI Recipe Chatbot (CPU Optimized)**

Deployed Website Link :- [https://receipebotjanardan.streamlit.app/](https://receipebotjanardan.streamlit.app/)  
Public GitHub Repository Link :-  https://github.com/Janardan3satpathy/Receipe\_bot

## **📌 Problem Statement**

**Objective:** Set up an AI model on a local server, fine-tune it, and build a chatbot interface.

**Key Deliverables:**

1. **Server Setup:** Install an open-source model (FLAN-T5-Small) suitable for limited resources (CPU).  
2. **Fine-Tuning:** Create a custom dataset of recipe ingredients and instructions, then train the model to learn the mapping between ingredients and full recipes.  
3. **API Integration:** Expose the trained model via a Python-based API (FastAPI) that accepts JSON queries and returns recipe suggestions.  
4. **Chatbot UI:** Develop a user-friendly web interface (Streamlit) that interacts with the API to display the conversation.  
5. **Offline Capability:** The entire system must be fully runnable on a standard Windows/Linux laptop without external internet dependencies after initial setup.

## **🚀 Quick Start Guide**

### **1\. Prerequisites**

* Python 3.8 or higher  
* Pip (Python Package Manager)  
* \~1GB of free disk space

### **2\. Installation**

Open your terminal/command prompt in the project folder and run:

pip install \-r requirements.txt

### **3\. Generate Data & Train**

Create the dataset and fine-tune the model on your CPU:

\# Step 1: Generate 500 synthetic recipe examples  
python data\_gen.py

\# Step 2: Train the model (Takes 5-10 mins on a standard laptop)  
python train.py

### **4\. Run the Application**

You need two separate terminal windows:

**Terminal 1 (Backend API):**

python api.py

*Wait until you see: "Uvicorn running on https://www.google.com/search?q=http://127.0.0.1:8000"*

**Terminal 2 (Frontend UI):**

streamlit run ui.py

*This will automatically open your web browser.*

### **5\. Verification**

* **Input:** Chicken, Rice, Salt  
* **Expected Output:** The AI will generate a recipe title and step-by-step instructions based on the training patterns (e.g., "Boiled Chicken with Rice...").

## **⚠️ NOTE: Scalability & Hardware Requirements**

This project uses a 500-item synthetic dataset and the FLAN-T5-Small model to ensure it runs smoothly on any standard laptop. Below is a breakdown of what happens if we scale this to a production-level dataset (e.g., 1 Million+ Recipes).

### **🔴 Scenario A: Running 1 Million Datasets on a Standard Laptop**

* **Hardware:** Standard CPU (Intel i5/i7 or Apple M1/M2), 8GB \- 16GB RAM, No dedicated GPU.  
* **Estimated Training Time:** 2 to 4 Weeks (Continuous running).  
* **Risk Factors:**  
  * **Overheating:** High risk of thermal throttling or hardware damage due to 100% CPU usage for days.  
  * **System Crash:** RAM will likely overflow (OOM Error) trying to process 1M+ records, causing the OS to freeze.  
* **Feasibility:** Impossible/Not Recommended.

### **🟢 Scenario B: Running 1 Million Datasets on Recommended Hardware**

To train a model on 1 million+ records effectively, you would need the following specifications:

* **Recommended Hardware:**  
  * **GPU:** NVIDIA RTX 3090 / 4090 (24GB VRAM) or A100 (40GB/80GB VRAM).  
  * **RAM:** 32GB \- 64GB System RAM.  
  * **Storage:** Fast NVMe SSD.  
* **Estimated Training Time:**  
  * Consumer GPU (RTX 3090/4090): \~12 to 24 Hours.  
  * Enterprise GPU (A100): \~2 to 5 Hours.  
* **Feasibility:** High. This is the standard setup for professional LLM fine-tuning.

### **Conclusion**

For this assignment, we utilize a 500-item synthetic dataset to demonstrate the architecture and mechanics of the solution (Data Pipeline \-\> Fine-Tuning \-\> API \-\> UI) without requiring enterprise-grade hardware.