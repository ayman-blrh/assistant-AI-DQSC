from pydantic import BaseModel, Field
from typing import Optional

class QARequest(BaseModel):
    """
    Modèle pour représenter une question envoyée par l’utilisateur.
    """
    question: str = Field(..., example="Qui est Kylian Mbappé ?")


class QAResponse(BaseModel):
    """
    Modèle pour la réponse renvoyée au client, incluant la réponse générée
    et la source documentaire.
    """
    answer: str = Field(..., example="Kylian Mbappé est un attaquant français...")
    source_content: Optional[str] = Field(None, example="Kylian Mbappé ...")
    source_name: Optional[str] = Field(None, example="kb_source.txt")


class ErrorResponse(BaseModel):
    """
    Modèle pour gérer les erreurs API de manière structurée.
    """
    error: str
    details: Optional[str] = None

class QAFolder(BaseModel):
    chemin : str 