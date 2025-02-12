import json
import os
import faiss
import numpy as np
import torch
import asyncio
import uuid
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForCausalLM, AutoTokenizer

# 🔹 Load FAISS (for fast similarity search)
FAISS_INDEX_FILE = "faiss_index.bin"
DATA_FILE = "knowledge_base.json"

# 🔹 Load Sentence Transformer Model (CPU-friendly)
embedding_model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")

# 🔹 Load LLaMA Model (Optimized for GPU if available)
model_name = "meta-llama/Llama-3.2-1B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32)
model.to(device)
model.eval()  # Set model to evaluation mode

# Ensure tokenizer has a padding token
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# 🔹 Create FAISS index for fast embedding lookup
embedding_size = 384  # Adjust according to the embedding model
faiss_index = faiss.IndexFlatL2(embedding_size)


# 🔹 Load knowledge base
async def load_knowledge_base():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


# 🔹 Save knowledge base
async def save_knowledge_base(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# 🔹 Process and store text chunks into FAISS
async def process_and_store_text(text, source, user_id):
    knowledge_base = await load_knowledge_base()

    # Split text into chunks
    chunk_size = 512
    words = text.split()
    chunks, current_chunk = [], []

    for word in words:
        if len(" ".join(current_chunk + [word])) <= chunk_size:
            current_chunk.append(word)
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    # Store embeddings in FAISS index
    embeddings = []
    record_id = str(uuid.uuid4())  # Generate a unique ID for this record
    for i, chunk in enumerate(chunks):
        embedding = embedding_model.encode(chunk).astype(np.float32)
        embeddings.append(embedding)

        # Corrected structure: Ensure each entry includes the text and the associated chunk data
        knowledge_base[f"{user_id}_{record_id}_{i}"] = {
            "text": chunk,
            "source": source,  # Optionally, you can store source info as well
            "chunk_index": i
        }

    # Convert list to NumPy array and add to FAISS index
    if embeddings:
        faiss_index.add(np.array(embeddings))

    await save_knowledge_base(knowledge_base)
    print(f"✅ Stored {len(chunks)} chunks from {source} with ID {record_id}")

    return record_id


# 🔹 Retrieve top-k relevant chunks using FAISS
async def retrieve_relevant_chunks(query, top_k=5):
    knowledge_base = await load_knowledge_base()
    query_embedding = embedding_model.encode(query).astype(np.float32).reshape(1, -1)

    # Find closest embeddings in FAISS
    distances, indices = faiss_index.search(query_embedding, top_k)
    relevant_chunks = []
    
    for i in indices[0]:
        if i < len(knowledge_base):
            entry = list(knowledge_base.values())[i]
            # Debugging: Ensure the entry has the 'text' key
            if "text" in entry:
                relevant_chunks.append(entry["text"])
            else:
                print(f"Warning: Missing 'text' in entry {entry}")

    return relevant_chunks

async def generate_response(user_query):
    relevant_chunks = await retrieve_relevant_chunks(user_query)

    if not relevant_chunks:
        return "I'm sorry, but I couldn't find relevant information. Please visit our website for more details."

    context = "\n".join(relevant_chunks)

    # Construct a precise prompt
    prompt = (
        f"User Question: {user_query}\n"
        f"Relevant Information: {context}\n\n"
        f"Provide only the necessary answer in a single sentence without additional context. If it's a cancellation request, give only the cancellation instructions."
    )

    inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True).to(device)

    with torch.no_grad():
        output = model.generate(
            inputs["input_ids"],
            attention_mask=inputs.get("attention_mask", None),
            pad_token_id=tokenizer.pad_token_id,
            max_new_tokens=50,  # Ensure short responses
            do_sample=True,  # Enable sampling for better responses
            temperature=0.5,  # Controlled randomness
            top_p=0.9
        )

    response = tokenizer.decode(output[0], skip_special_tokens=True).strip()

    # Ensure response is relevant and direct
    if not response or "Relevant Information:" in response:
        return "To cancel your lawn care plan, please fill out the cancellation form on our website. [cancel_plan]"

    return response

# 🔹 FastAPI Setup
app = FastAPI()

class QueryRequest(BaseModel):
    query: str
    filename: str
    user_id: str  # Added user_id field for more personalized responses

@app.post("/chatbot/")
async def chatbot(request: QueryRequest):
    filename = request.filename
    user_id = request.user_id

    if not os.path.isfile(filename):
        return {"error": f"File {filename} not found on the server."}

    with open(filename, 'r') as f:
        text_content = f.read()

    record_id = await process_and_store_text(text_content, filename, user_id)
    response = await generate_response(request.query)

    # After responding, delete the knowledge base entry associated with the user's query
    knowledge_base = await load_knowledge_base()
    for key in list(knowledge_base.keys()):
        if key.startswith(f"{user_id}_{record_id}"):
            del knowledge_base[key]

    await save_knowledge_base(knowledge_base)
    
    return {"response": response}

