from app.db.database import SessionLocal
from app.db.models import EventLog


def save_event(
    event: str,
    user_id: str,
    product_id=None,
    category_code=None,
    co2_data=None,
    ai_result=None
):
    db = SessionLocal()
    try:
        record = EventLog(
            event=event,
            user_id=user_id,
            product_id=product_id,
            category_code=category_code,
            co2_data=co2_data,
            ai_result=ai_result
        )
        db.add(record)
        db.commit()
    finally:
        db.close()
