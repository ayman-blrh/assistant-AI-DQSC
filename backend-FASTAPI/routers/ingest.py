import os
from fastapi import APIRouter, HTTPException , UploadFile , File
from fastapi.responses import JSONResponse
from services.ingestion import ingest_document as iDOC , ingest_folder as iFOD
from schemas.qa import QAFolder
from services.ingestion import upload_file

router = APIRouter()

@router.post("/ingest")
async def ingest_route(file: UploadFile = File(...)):
    """
    Endpoint HTTP pour lancer l'ingestion de documents dans Qdrant.
    Reçoit en entrée :
      - data_folder : dossier à ingérer (ex. data/)
      - collection_name : nom de la collection Qdrant
    """
    collection_name: str = "vector_db"
    data_folder = file.filename
    
    try:
        upload_file(file)

        return JSONResponse(status_code=200, content={
            "status": "success",
            "detail": f"Ingested documents from '{data_folder}' into collection '{collection_name}'."
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))