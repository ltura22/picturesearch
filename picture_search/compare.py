import json

import faiss
import numpy as np
from sklearn.preprocessing import MinMaxScaler

from picture_search.georgian_embedding import calculate_embedding
import stanza
import pickle

from scipy.special import softmax


# Keyword gen
stanza.download('ka')
nlp = stanza.Pipeline('ka')

def advanced_tokenize_georgian(text):
    # Process the Georgian text
    doc = nlp(text)
    # Extract tokens with additional information
    tokens = []
    for sentence in doc.sentences:
        for word in sentence.words:
            tokens.append(word.lemma)  # Use word.lemma if you prefer lemmatized tokens
    return tokens

with open('bm25_model.pkl', 'rb') as f:
    data = pickle.load(f)
    bm25 = data['bm25']
    tokenized_documents = data['documents']

with open("data.json", "r") as f:
    names = json.load(f)

query = 'ცხენზე ზის კატა'
k = 10
n = len(tokenized_documents)

def search_photos(query, k=10):
    query_emb = calculate_embedding(query)
    query_vector = np.array([query_emb]).astype('float32')

    indx = faiss.read_index("faiss_index.faiss")

    d, i = indx.search(query_vector, min(2*k, n))
    for ix,dx in zip(i[0],d[0]):
        print(ix, names[str(ix)], dx)

    faiss_pairs = list(zip(i[0], d[0]))
    sorted_faiss_pairs_by_index = sorted(faiss_pairs, key=lambda x: x[0])

    print('-' * 40)

    tokenized_query = advanced_tokenize_georgian(query)
    print(f"Tokenized query: {tokenized_query}")
    bm25_scores = bm25.get_scores(tokenized_query)

    print('-' * 40)
    print("BM25 Scores:", bm25_scores)
    for ix, score in enumerate(bm25_scores):
        print(f"Document Index: {ix}, BM25 Score: {score}")

    filtered_bm25_scores = [(ix, bm25_scores[ix]) for ix in i[0] if ix < len(bm25_scores)]
    sorted_bm25_pairs_by_index = sorted(filtered_bm25_scores, key=lambda x: x[0])

    sorted_scores = sorted(filtered_bm25_scores, key=lambda x: x[1], reverse=True)

    for idx, score in sorted_scores:
        print(f"Document Index: {idx}, BM25 Score: {score}")

    # Normalize BM25 scores
    bm25_scores = np.array([x[1] for x in sorted_bm25_pairs_by_index])
    bm25_normalized = MinMaxScaler().fit_transform(bm25_scores.reshape(-1, 1)).flatten()

    # Normalize FAISS similarity scores
    faiss_scores = np.array([x[1] for x in sorted_faiss_pairs_by_index])  # FAISS distances
    faiss_normalized = MinMaxScaler().fit_transform(faiss_scores.reshape(-1, 1)).flatten()

    # Combine scores with weights
    alpha = 0.7  # Weight for BM25 (adjust as needed)
    combined_scores = alpha * bm25_normalized + -1 * (1 - alpha) * faiss_normalized
    combined_scores = (1 + combined_scores) * 50
    combined_scores_and_index = list(zip([x[0] for x in sorted_faiss_pairs_by_index], combined_scores, bm25_scores, faiss_scores))

    print(f"Combined Scores:{combined_scores}")

    # Sort combined scores in descending order
    sorted_combined = sorted(combined_scores_and_index, key=lambda x: x[1], reverse=True)
    sorted_combined = sorted_combined[:k]  # Limit to top k results
    # Print the sorted results
    for idx, score, bm25_score, faiss_score in sorted_combined:
        print(f"Document Index: {idx}, Combined Score: {score}, BM25 Score: {bm25_score}, FAISS Score: {faiss_score}")

    return sorted_combined

def search_wrapper(query, k=10):
    search_results = search_photos(query, k)

    # Extract paths and combined scores
    paths = [names[str(result[0])]['path'] for result in search_results]
    combined_scores = [result[1] for result in search_results]

    # Apply softmax to the combined scores
    normalized_scores = softmax(combined_scores)

    # Combine paths with their normalized scores
    results_with_paths = list(zip(paths, normalized_scores * 100))

    return results_with_paths

results = search_wrapper(query, k)
print('-' * 40)

for path, score in results:
    print(f"Path: {path}, Score: {score:.4f}")

