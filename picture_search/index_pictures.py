import json

import faiss
import numpy as np
from description import get_description
from picture_search.georgian_embedding import calculate_embedding
from translate_ge import translate_en_to_ka
from time import time
import os
import json

import stanza
from rank_bm25 import BM25Okapi
import pickle

# Keyword gen
stanza.download('ka')
nlp = stanza.Pipeline('ka')

PICTURE_DIRECTORY = "../small_data/"
VECTOR_DIMENSION = 384


def advanced_tokenize_georgian(text):
    # Process the Georgian text
    doc = nlp(text)
    # Extract tokens with additional information
    tokens = []
    for sentence in doc.sentences:
        for word in sentence.words:
            tokens.append(word.lemma)  # Use word.lemma if you prefer lemmatized tokens
    return tokens

def index_pictures():
    faiss_index = faiss.IndexFlat(VECTOR_DIMENSION)
    emb_list = []
    names = {}
    tokenized_descs = []
    i = 0
    for root, _, files in os.walk(PICTURE_DIRECTORY):
        for file in files:
            image_path = os.path.join(root, file)
            image_description = get_description(image_path)
            image_description_ge = translate_en_to_ka(image_description)
            print(image_description_ge)
            print(image_path)
            emb = calculate_embedding(image_description_ge)
            emb_list.append(emb)
            keywords = advanced_tokenize_georgian(image_description_ge)
            names[i] = {
                "path": image_path,
                "description": image_description_ge,  # No .encode('utf-8')
                "keywords": keywords,  # No .encode('utf-8') for each keyword
            }
            tokenized_descs.append(keywords)
            i += 1

    bm25 = BM25Okapi(tokenized_descs)

    with open('bm25_model.pkl', 'wb') as f:
        pickle.dump({'bm25': bm25, 'documents': tokenized_descs}, f)

    with open('data.json', 'w', encoding='utf-8') as json_file:  # Ensure UTF-8 encoding
        json.dump(names, json_file, indent=4, ensure_ascii=False)  # Use ensure_ascii=False to preserve Unicode characters

    embeddings = np.array(emb_list).astype('float32')
    faiss_index.add(embeddings)
    faiss.write_index(faiss_index, "faiss_index.faiss")


if __name__ == "__main__":
    start_time = time()
    index_pictures()
    end_time = time()
    print(f"Indexing completed in {end_time - start_time:.2f} seconds.")