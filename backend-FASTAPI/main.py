import os
from fastapi import FastAPI
from routers.qa import router as qa_router
from routers.ingest import router as ingest_router
from fastapi.middleware.cors import CORSMiddleware

def create_app() -> FastAPI:
    """
    Créée l’application FastAPI, inclut les routeurs et ajoute la configuration nécessaire.
    """
    app = FastAPI(
        title="Chatbot RAG avec FastAPI & LangChain",
        description="API pour QA augmentée par retrieval à partir de documents",
        version="1.0.0"
    )

    origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200"
    ]
    # Ajout du middleware CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,        # Autorise ces origines
        allow_credentials=True,       # Autorise l'envoi de cookies ou tokens
        allow_methods=["*"],          # Autorise toutes les méthodes (GET, POST, etc.)
        allow_headers=["*"],          # Autorise tous les headers
    )

    # Charger d'éventuelles variables d'environnement ou middleware ici
    # Exemple : CORS, authentification, etc.
    app.include_router(qa_router, prefix="", tags=["qa"])
    app.include_router(ingest_router, prefix="", tags=["ingestion"])

    return app

app = create_app()

# Optionnel : point d’entrée si on lance directement ce fichier
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)), reload=True)
