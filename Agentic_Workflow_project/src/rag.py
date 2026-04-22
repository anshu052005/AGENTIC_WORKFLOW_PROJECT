import json
import os
import numpy as np
import faiss
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from google import genai


# =========================
# CONFIG
# =========================
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

EMBED_MODEL = "all-MiniLM-L6-v2"
LLM_MODEL = "gemini-2.5-flash"


# =========================
# DOCUMENT LOADER
# =========================
class DocumentLoader:
    def __init__(self, path):
        self.path = path

    def load(self):
        with open(self.path, "r") as f:
            data = json.load(f)
        return data["documents"]


# =========================
# EMBEDDING MODEL
# =========================
class EmbeddingModel:
    def __init__(self):
        self.model = SentenceTransformer(EMBED_MODEL)

    def encode(self, texts):
        return np.array(self.model.encode(texts)).astype("float32")


# =========================
# VECTOR STORE (FAISS)
# =========================
class VectorStore:
    def __init__(self, embeddings):
        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(embeddings)

    def search(self, query_embedding, k=2):
        _, indices = self.index.search(query_embedding, k)
        return indices[0]


# =========================
# RAG PIPELINE
# =========================
class RAGPipeline:
    def __init__(self, data_path):
        self.loader = DocumentLoader(data_path)
        self.embedder = EmbeddingModel()

        self.documents = self.loader.load()
        self.doc_embeddings = self.embedder.encode(self.documents)

        self.vector_store = VectorStore(self.doc_embeddings)

        self.client = genai.Client(api_key=API_KEY)

    def retrieve(self, query, k=2):
        query_embedding = self.embedder.encode([query])
        indices = self.vector_store.search(query_embedding, k)
        return [self.documents[i] for i in indices]


    def generate(self, query, state):

        context = self.retrieve(query)

        # 🔹 last 5 conversations
        history_text = "\n".join(
            [f"{msg['role']}: {msg['content']}" for msg in state.history[-5:]]
        )

        prompt = f"""
    You are an AI assistant for AutoStream.

    Conversation History:
    {history_text}

    Use ONLY this context:
    {context}

    Answer the question:
    {query}

    If answer not found, say: I don't have that information.
    """

        for _ in range(3):
            try:
                response = self.client.models.generate_content(
                    model=LLM_MODEL,
                    contents=prompt
                )
                return response.text
            except:
                import time
                time.sleep(2)

        return "Temporary issue, try again."

    def query(self, user_query, state):
        return self.generate(user_query, state)