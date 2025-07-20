import json

import stanza
from rank_bm25 import BM25Okapi
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize
from sentence_transformers import SentenceTransformer
import numpy as np

# Download and load the Georgian pipeline
stanza.download('ka')
nlp = stanza.Pipeline('ka')

def advanced_tokenize_georgian(text):
    # Process the Georgian text
    doc = nlp(text)
    print(f"Processed document: {doc}")
    # Extract tokens with additional information
    tokens = []
    for sentence in doc.sentences:
        for word in sentence.words:
            tokens.append(word.lemma)  # Use word.lemma if you prefer lemmatized tokens
    return tokens

# # Example usage
# first_text = "ყავისფერი ცხენი რომელიც მწვანე ველის გავლით მიდის"
# second_text = "ქუჩაზე თეთრი ხაზები"
# first_tokens = advanced_tokenize_georgian(first_text)
# second_tokens = advanced_tokenize_georgian(second_text)
# print(f"First tokens: {first_tokens}")
# print(f"Second tokens: {second_tokens}")
#
# bm25 = BM25Okapi([first_tokens])
# bm25_scores = bm25.get_scores(first_tokens)
# print(f"BM25 scores for first text: {bm25_scores}")
# bm25_scores = bm25.get_scores([ "ბალი"])
# print(f"BM25 scores for 'ბალი': {bm25_scores}")

# Tokenize the documents
with open("data.json") as f:
    data = json.load(f)
documents = [x['description'] for x in data.values()]
tokenized_documents = [advanced_tokenize_georgian(doc) for doc in documents]

# Initialize BM25
bm25 = BM25Okapi(tokenized_documents)

# Example query
query = "ცხენი"
tokenized_query = advanced_tokenize_georgian(query)

# Calculate BM25 scores
bm25_scores = bm25.get_scores(tokenized_query)
print("BM25 Scores:", bm25_scores)