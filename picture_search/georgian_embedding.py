import numpy as np
from sentence_transformers import SentenceTransformer
import os

cache_dir = 'georgian_embedding_model'
model_path = os.path.join(cache_dir, 'models--sentence-transformers--paraphrase-multilingual-MiniLM-L12-v2/snapshots/86741b4e3f5cb7765a600d3a3d55a0f6a6cb443d')

if os.path.exists(model_path):
    model = SentenceTransformer(model_path)
else:
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2', cache_folder=cache_dir)

def get_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def calculate_embedding(text):
    return model.encode(text)