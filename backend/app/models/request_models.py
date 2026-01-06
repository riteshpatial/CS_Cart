from pydantic import BaseModel
from typing import Optional

class CSCartEvent(BaseModel):
    event: str
    user_id: str
    product: Optional[str] = None
    category: Optional[str] = None
    search_query: Optional[str] = None
