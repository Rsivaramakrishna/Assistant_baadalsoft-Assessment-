from flask import Flask, render_template, request, jsonify
import json
import numpy as np
import ollama
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

print("Starting application...")

app = Flask(__name__)

# -----------------------------
# Load embedding model
# -----------------------------
print("Loading embedding model...")

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

print("Embedding model loaded")


# -----------------------------
# Chunk documents
# -----------------------------
def chunk_text(text, size=80):
    words = text.split()
    chunks = []
    for i in range(0, len(words), size):
        chunks.append(" ".join(words[i:i + size]))
    return chunks


# -----------------------------
# Load docs
# -----------------------------
print("Loading documents...")

with open("docs.json") as f:
    docs = json.load(f)

doc_chunks = []
doc_embeddings = []

for doc in docs:

    text = doc["title"] + " " + doc["content"]

    chunks = chunk_text(text)

    for chunk in chunks:

        emb = embedding_model.encode(chunk)

        doc_chunks.append(chunk)

        doc_embeddings.append(emb)

# FIXED LINE
doc_embeddings = np.array(doc_embeddings)

print("Documents processed:", len(doc_chunks))


# -----------------------------
# Retrieve context
# -----------------------------
def retrieve_context(query):

    query_embedding = embedding_model.encode(query)

    similarities = cosine_similarity([query_embedding], doc_embeddings)[0]

    top_indices = similarities.argsort()[-3:][::-1]

    context = ""

    for i in top_indices:
        context += doc_chunks[i] + "\n"

    return context


# -----------------------------
# Generate Answer with Ollama
# -----------------------------
def generate_answer(context, question):

    prompt = f"""
You are a helpful AI assistant.

Use ONLY the context below to answer.

Context:
{context}

Question:
{question}
"""

    response = ollama.chat(
        model="tinyllama",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response["message"]["content"]


# -----------------------------
# Routes
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    user_message = request.json["message"]

    context = retrieve_context(user_message)

    answer = generate_answer(context, user_message)

    return jsonify({"response": answer})


# -----------------------------
# Run Server
# -----------------------------
if __name__ == "__main__":

    print("Starting Flask server...")

    app.run(debug=True)