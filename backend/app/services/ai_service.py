def generate_ai_response(event: str, details: str):
    """
    Central AI decision layer
    This will later be replaced by OpenAI / LLM logic
    """

    # -------------------------
    # PRODUCT VIEW
    # -------------------------
    if event == "product_view":
        return {
            "type": "similar_products",
            "title": "Users also viewed",
            "items": [
                "iPhone 15 Pro",
                "iPhone 14 Plus",
                "Samsung S23 Ultra"
            ]
        }

    # -------------------------
    # SEARCH
    # -------------------------
    if event == "search":
        return {
            "type": "search_recommendation",
            "title": "Recommended products",
            "items": [
                "iPhone 15",
                "iPhone 14",
                "Samsung S23"
            ]
        }

    # -------------------------
    # ADD TO CART  ✅ FIXED
    # -------------------------
    if event == "add_to_cart":
        return {
            "type": "eco_alternatives",
            "title": "Lower CO2 alternatives",
            "items": [
                "Organic Cotton T-Shirt",
                "Recycled Polyester T-Shirt",
                "Hemp Blend T-Shirt"
            ]
        }

    # -------------------------
    # FALLBACK
    # -------------------------
    return {
        "type": "unknown_event",
        "message": "No recommendation available"
    }
