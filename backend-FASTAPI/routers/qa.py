from fastapi import APIRouter, HTTPException
from schemas.qa import QARequest, QAResponse, ErrorResponse
from services.qa_service_gemini import ask_question_gemini as gemn

router = APIRouter()

@router.post("/ask", response_model=QAResponse, responses={400: {"model": ErrorResponse}})
async def ask_endpoint(payload: QARequest):
    """
    Endpoint pour poser une question.
    Reçoit un payload `QARequest`, appelle ask_question(),
    et renvoie `QAResponse` ou `ErrorResponse`.
    """
    try:
        """answer, source_content, source_name = ask_question(payload.question)"""
        answer, source_content, source_name = gemn(payload.question)
        return QAResponse(
            answer=answer,
            source_content=source_content,
            source_name=source_name
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
