import os
import json
import numpy as np #Import numpy
from sentence_transformers import SentenceTransformer
from langchain.vectorstores import FAISS
from tqdm import tqdm

# File paths
CHUNKS_FILE = "text_chunks.json"
FAISS_DB_PATH = "lord_of_mysteries_db"
EMBEDDINGS_FILE = "embeddings.npy" # Add embedding numpy output

# Load text chunks (Skip Markdown processing)
try:
    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        chunks = json.load(f)
    print(f"✅ Loaded {len(chunks)} chunks successfully!")
except FileNotFoundError:
    print(f"❌ Error: Could not find {CHUNKS_FILE}.  Make sure it exists.")
    exit()
except json.JSONDecodeError:
    print(f"❌ Error: Could not decode {CHUNKS_FILE}.  Check if it's valid JSON.")
    exit()
except Exception as e:
    print(f"❌ Error loading {CHUNKS_FILE}: {e}")
    exit()

# Check if FAISS database already exists
if os.path.exists(FAISS_DB_PATH) and os.path.exists(EMBEDDINGS_FILE):  #Check if embeddings file exits, you do not want to generate vector
    print("✅ FAISS database and embeddings file already exist! Skipping embedding generation.")
    print("Loading embeddings from File") #printing that it is getting read to notify the user

    hf_embeddings = SentenceTransformer("all-MiniLM-L6-v2") #instantiate the model if needed
    embeddings = np.load(EMBEDDINGS_FILE, allow_pickle=True)
    #**Create vector_store, use the same db
    vector_store = FAISS.from_embeddings(text_embeddings=list(zip(chunks, embeddings)), embedding_function=hf_embeddings)
else:
    print("🔄 FAISS database or Embeddings files not found. Generating embeddings...")
    hf_embeddings = SentenceTransformer("all-MiniLM-L6-v2")

    # Generate embeddings with a progress bar and Save embeddings on Np Format

    embeddings = [hf_embeddings.encode(chunk) for chunk in tqdm(chunks, desc="Processing Embeddings")]

    print("✅ Text chunks converted to embeddings successfully!")
    np.save(EMBEDDINGS_FILE, embeddings)
    #**Correct FAISS storage, now vector can be stored correctly, with text and embeddings

    vector_store = FAISS.from_embeddings(embeddings, chunks)  # ✅ Correct
    vector_store.save_local(FAISS_DB_PATH)
    print(f"✅ Vector database saved at: {FAISS_DB_PATH}")



try:
    vector_store.save_local(FAISS_DB_PATH) #The problem before may be caused because if the vector files already exits, they would be overwritten
    print(f"✅ Vector database saved at: {FAISS_DB_PATH}")

except Exception as e:
    print(f"Error saving Faiss, it may exist: {e}")