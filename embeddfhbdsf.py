import os
import json
import pickle
from sentence_transformers import SentenceTransformer
from langchain.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from tqdm import tqdm

# File paths remain the same
CHUNKS_FILE = "text_chunks.json"
EMBEDDINGS_FILE = "embeddings.pkl"
FAISS_DB_PATH = "lord_of_mysteries_db"

# Load text chunks
with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
    chunks = json.load(f)
print(f"✅ Loaded {len(chunks)} chunks successfully!")

# Create HuggingFaceEmbeddings instance
embeddings_model = HuggingFaceEmbeddings()

# Rest of your embedding generation code remains the same...
if os.path.exists(EMBEDDINGS_FILE):
    print("✅ Found existing embeddings file. Loading embeddings...")
    with open(EMBEDDINGS_FILE, "rb") as f:
        embeddings = pickle.load(f)
    print(f"✅ Loaded {len(embeddings)} embeddings successfully!")
else:
    print("🔄 No saved embeddings found. Generating embeddings...")
    embeddings = [embeddings_model.embed_documents(chunk)[0] for chunk in tqdm(chunks, desc="Processing Embeddings")]
    print("✅ Text chunks converted to embeddings successfully!")
    with open(EMBEDDINGS_FILE, "wb") as f:
        pickle.dump(embeddings, f)
    print(f"✅ Embeddings saved to {EMBEDDINGS_FILE}")

# FAISS setup
if os.path.exists(FAISS_DB_PATH):
    print("✅ FAISS database already exists! Skipping FAISS setup.")
else:
    print("🔄 FAISS database not found. Creating FAISS index...")
    vector_store = FAISS.from_texts(
        texts=chunks,
        embedding=embeddings_model
    )
    vector_store.save_local(FAISS_DB_PATH)
    print(f"✅ Vector database saved at: {FAISS_DB_PATH}")