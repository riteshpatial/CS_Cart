from pydantic import BaseModel

class CSCartEvent(BaseModel):
    event: str
    user_id: str
    product: str
    category: str
    search_query: str
