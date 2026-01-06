from fastapi import APIRouter
from app.schemas.cscart import CSCartEvent
from app.services.ai_service import generate_ai_response
from app.utils.prompt_builder import build_prompt

router = APIRouter(prefix="/events", tags=["CS-Cart"])

@router.post("/cscart")
def cscart_event(event: CSCartEvent):
    prompt = build_prompt(
        event.event,
        f"""
User: {event.user_id}
Product: {event.product}
Category: {event.category}
Search: {event.search_query}
"""
    )
    return generate_ai_response(prompt)
