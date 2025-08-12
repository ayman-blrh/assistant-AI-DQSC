## 📌 Objectif
Ce projet met en place un système de **Retrieval-Augmented Generation (RAG)** où un **LLM** (Gemini) génère des réponses enrichies à partir de documents indexés dans **Qdrant**.  
L'application est composée d'un **frontend Angular** pour l'UI et d'un **backend FastAPI** pour la logique et l'orchestration.

## 🏗 Fonctionnement Global

1. **L'utilisateur pose une question** via l'interface Angular.
2. **FastAPI** reçoit la requête et génère les **embeddings** de la question.
3. **Qdrant** est interrogé pour trouver les documents les plus pertinents grâce à la recherche vectorielle.
4. Les documents pertinents sont ajoutés au **prompt** envoyé au **LLM Gemini**.
5. **Gemini** produit une réponse contextuelle et optimisée.
6. La réponse est renvoyée et affichée dans l'UI Angular.

## ⚙️ Architecture Technique
<img width="1024" height="1024" alt="archi" src="https://github.com/user-attachments/assets/fbafa4bb-f4f2-4753-b643-f358cce731d9" />

## 📦 Stack
- **Frontend** : Angular
- **Backend** : FastAPI (Python)
- **LLM** : Gemini (Google)
- **Base vectorielle** : Qdrant ( docker )

## 🚀 Installation

1️⃣ Cloner le projet
  git clone <URL_DU_PROJET>
  cd <NOM_DU_REPO>
  
2️⃣ Lancer Qdrant
  docker run -d --name qdrant_container -p 6333:6333 qdrant/qdrant:dev
  Qdrant est disponible sur http://localhost:6333.

3️⃣ Lancer le backend (FastAPI)
  cd backend
  pip install -r requirements.txt
  uvicorn main:app --reload
  Backend accessible sur http://localhost:8000.

4️⃣ Lancer le frontend (Angular)
  cd frontend
  npm install
  ng serve
  UI disponible sur http://localhost:4200.
