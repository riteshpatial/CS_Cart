from fastapi import APIRouter
from app.schemas.ai import AIRequest, AIResponse
from app.services.ai_service import generate_ai_response

router = APIRouter(prefix="/ai", tags=["AI"])

@router.post("/generate", response_model=AIResponse)
def generate_ai(request: AIRequest):
    result = generate_ai_response(
        event=request.event,
        details=request.details
    )
    return {"result": result}
