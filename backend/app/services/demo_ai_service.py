class DemoAIService:
    def generate(self, event: str, details: str) -> dict:

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

        if event == "cart_abandon":
            return {
                "type": "cart_reminder",
                "message": "Complete your purchase now and get 10% off!"
            }

        return {
            "type": "unknown_event",
            "message": "No recommendation available"
        }
