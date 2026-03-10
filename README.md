# Assistant_baadalsoft-Assessment
Production Grade GenAI Assistant using Retrieval Augmented Generation (RAG)
1. Introduction

This document explains the design and implementation of a Generative AI assistant built using the Retrieval Augmented Generation (RAG) architecture. 
The objective of the project is to build a chatbot that can answer user queries using a custom document knowledge base instead of relying only on 
the pre‑trained knowledge of a large language model.

Traditional LLM based chatbots generate answers based only on their training data. While this can be powerful, it also introduces a major problem 
called hallucination. The model may generate incorrect answers that sound confident but are not grounded in real data. Retrieval Augmented 
Generation solves this problem by first retrieving relevant information from a knowledge base and then passing that information as context to the 
language model.

In this project the system is implemented using Python with the Flask framework. A simple web interface allows users to ask questions. The system 
processes the question, searches the knowledge base using vector similarity search, retrieves the most relevant document chunks, and then sends 
the context to a local Large Language Model running through Ollama.

The advantage of using Ollama is that it allows the application to run local AI models such as TinyLlama, Phi3 or Llama3 without requiring an 
external API. This makes the system free to use and removes dependency on cloud services such as OpenAI or Gemini.

The overall system combines several modern AI technologies including sentence embeddings, vector similarity search, local language models, 
and web‑based chat interfaces. Together these components form a practical implementation of a production style GenAI assistant.

2. System Architecture

The system architecture follows the standard Retrieval Augmented Generation pipeline. The application can be divided into several major 
components which work together to produce intelligent responses.

The first component is the document knowledge base. In this project the knowledge base is stored in a JSON file called docs.json. Each document 
contains a title and a content field describing a piece of information that the assistant can answer questions about.

The second component is document preprocessing. Large documents are split into smaller pieces called chunks. This is necessary because embedding 
models work best when processing small pieces of text rather than entire documents. Chunking also improves search accuracy because the system 
can retrieve only the relevant portion of a document.

The third component is the embedding generation stage. Each text chunk is converted into a vector representation using a sentence embedding 
model from the Sentence Transformers library. These vectors represent the semantic meaning of the text.

The fourth component is the vector similarity search. When a user asks a question, the system converts the question into an embedding vector and 
compares it with the stored document vectors using cosine similarity. The most relevant document chunks are retrieved.

The final component is response generation. The retrieved context is combined with the user’s question and sent to the Ollama language model. 
The model generates a response that is grounded in the retrieved information. This ensures that answers remain accurate and relevant to the 
knowledge base.

This modular architecture makes the system scalable and easy to extend. Additional documents can be added to the knowledge base without 
changing the core application logic.

3. Technology Stack

The project uses several modern tools and libraries to implement the RAG system.

Python serves as the primary programming language because it provides strong support for machine learning and web development. Python also has 
an extensive ecosystem of libraries for working with AI models.

Flask is used as the backend web framework. Flask is lightweight and simple, making it ideal for building APIs and web applications. In this 
project Flask handles routing, processes user input, and returns responses to the frontend.

Sentence Transformers provides the embedding model used for semantic search. The model all‑MiniLM‑L6‑v2 is used because it is efficient and 
provides high quality sentence embeddings while consuming relatively little memory.

NumPy is used to store and manipulate embedding vectors. Since embeddings are numerical arrays, NumPy provides efficient operations for vector 
storage and computation.

Scikit‑learn is used for calculating cosine similarity between vectors. Cosine similarity measures how similar two vectors are in a high 
dimensional space.

Ollama is used to run the large language model locally. Instead of sending requests to external APIs, the system interacts with a local LLM 
through the Ollama Python library. Lightweight models such as TinyLlama can run even on systems with limited RAM.

The frontend interface is implemented using HTML, CSS and JavaScript. This provides a simple chat interface where users can type questions and 
receive responses from the AI assistant.

4. Document Processing and Chunking

Document preprocessing is a critical step in the RAG pipeline. Large documents must be divided into smaller segments so that they can be 
processed effectively by the embedding model.

In this project the chunk_text function is used to split documents into smaller pieces. The function takes a block of text and divides it into 
groups of approximately eighty words. Each group becomes a separate chunk.

Chunking improves the retrieval process in several ways. First, it ensures that embeddings capture the meaning of specific sections of text 
rather than entire documents. Second, it allows the system to retrieve only the relevant information instead of returning unnecessary content.

For example, consider a document that contains information about password resets, account creation, and billing. If a user asks about password 
reset procedures, the system should retrieve only the password section rather than the entire document. Chunking makes this possible.

Once chunking is complete, each chunk is converted into an embedding vector. These embeddings are stored along with the original text so that 
they can be retrieved later during the similarity search stage.

5. Embedding Generation

Embeddings are numerical representations of text that capture semantic meaning. Instead of representing text as simple keywords, embeddings 
map sentences into a high dimensional vector space where similar meanings appear closer together.

The project uses the all‑MiniLM‑L6‑v2 model from the Sentence Transformers library. This model is designed for sentence similarity tasks and 
produces embeddings that represent semantic meaning effectively.

Each text chunk from the knowledge base is passed into the embedding model using the encode() function. The model returns a numerical vector 
containing hundreds of values. These vectors are stored in a list and later converted into a NumPy array for efficient processing.

When a user asks a question, the same embedding model converts the query into a vector representation. Because both the query and the document 
chunks exist in the same vector space, the system can measure similarity between them.

6. Similarity Search

Similarity search is the process used to identify which document chunks are most relevant to the user's question.

The system calculates cosine similarity between the query embedding and every stored document embedding. Cosine similarity measures the angle 
between two vectors. A value closer to one indicates a higher degree of similarity.

After calculating similarity scores for all document chunks, the system sorts the results and selects the top three most relevant chunks. 
These chunks are combined to form the context that will be passed to the language model.

This retrieval step is the key feature that differentiates RAG systems from traditional LLM chatbots. Instead of relying solely on the model’s 
training data, the system dynamically retrieves information from the knowledge base.

7. Response Generation using Ollama

After the relevant document chunks are retrieved, the system constructs a prompt for the language model. The prompt includes both the retrieved 
context and the user’s question.

The prompt instructs the model to answer using only the provided context. This prevents the model from generating unrelated or incorrect 
information.

The prompt is sent to the Ollama model using the ollama.chat() function. Ollama runs the language model locally and returns a generated response.

Using a local model has several advantages. It eliminates API costs, improves privacy by keeping data on the local machine, and ensures that 
the system can operate without internet connectivity.

8. Web Application Interface

The Flask web framework handles communication between the frontend and backend. The main route renders the chat interface where users can 
enter questions.

When a user submits a message, JavaScript sends a POST request to the Flask backend. The backend processes the message using the RAG pipeline 
and returns a JSON response containing the generated answer.

The frontend then displays the assistant’s response in the chat window. This interaction creates a conversational experience similar to modern 
AI assistants.

9. Conclusion

This project demonstrates how a production style GenAI assistant can be built using Retrieval Augmented Generation. By combining document 
embeddings, similarity search, and local language models, the system can answer user questions accurately using a custom knowledge base.

The architecture is scalable and can be extended with more advanced components such as vector databases, conversation memory, streaming 
responses, and cloud deployment.

Overall, the project provides a strong foundation for building intelligent knowledge assistants for organizations, educational systems, and 
customer support platforms.

