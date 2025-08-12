import os
from langchain import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_qdrant import Qdrant
from qdrant_client import QdrantClient
from langchain_huggingface import HuggingFaceEmbeddings
from google import genai as gn2
from google.genai import types
import google.generativeai as genai
# 🇫🇷 Charger le modèle LLM quantifié localement
my_api_key ="AIzaSyA9fJSTtpyDaV_oDHH5IDVzpWJJE5vHRC8"
genai.configure(api_key=my_api_key)

# 1) Modèle de génération (simple, stable)
llm = genai.GenerativeModel("gemini-2.5-flash")

# 2) Embeddings (⚠️ doivent matcher l’index utilisé à l’ingestion)
# Si tu as indexé avec all-mpnet-base-v2, garde-le aussi ici.
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# 3) Qdrant
client = QdrantClient(url=os.getenv("QDRANT_URL", "http://localhost:6333"), prefer_grpc=False)
collection_name = os.getenv("QDRANT_COLLECTION", "vector_db")

vector_store = Qdrant(
    client=client,
    embeddings=embeddings,
    collection_name=collection_name
)

# k plus large pour améliorer le rappel
retriever = vector_store.as_retriever(search_kwargs={"k": 8})

# 4) Prompt propre
prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=(
        "Tu es un assistant spécialisé. Réponds UNIQUEMENT avec les informations du CONTEXTE.\n"
        "Si l'information n'est pas dans le contexte, dis : \"Je ne sais pas d'après les documents.\"\n"
        "Style: clair et concis en français.\n\n"
        "=== CONTEXTE ===\n{context}\n\n"
        "=== QUESTION ===\n{question}\n"
    )
)

def ask_question_gemini(question: str):
    # 1) Récupération
    docs = retriever.get_relevant_documents(question)
    if not docs:
        context = "Aucun document pertinent trouvé."
    else:
        # Injecter texte + source dans le contexte
        parts = []
        for i, d in enumerate(docs, 1):
            src = d.metadata.get("source") or d.metadata.get("file_path") or d.metadata.get("title") or "source_inconnue"
            parts.append(f"[CHUNK {i}] [source: {src}]\n{d.page_content}")
        context = "\n\n---\n\n".join(parts)

    # 2) Prompt final
    full_prompt = prompt.format(context=context, question=question)

    # 3) Appel Gemini (SDK unique)
    try:
        resp = llm.generate_content(full_prompt)
        answer = resp.text.strip() if getattr(resp, "text", None) else "Je n'ai pas pu générer de réponse."
    except Exception as e:
        answer = f"Erreur lors de l'appel à Gemini : {e}"

    # 4) Renvoyer quelques infos utiles pour debug
    top_source = docs[0].metadata.get("source", "") if docs else "Aucune source disponible."
    return answer, context, top_source

# (Optionnel) petite fonction de debug pour voir les scores
def debug_search(query: str, k: int = 5):
    from qdrant_client.models import SearchParams
    # Embedding de la requête (même modèle que ci-dessus)
    q_vec = embeddings.embed_query(query)
    hits = client.search(
        collection_name=collection_name,
        query_vector=q_vec,
        limit=k,
        search_params=SearchParams(hnsw_ef=128, exact=False)
    )
    for i, h in enumerate(hits, 1):
        src = (h.payload or {}).get("source")
        print(i, "score:", round(h.score, 4), "source:", src)
