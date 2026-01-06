def build_prompt(event: str, details: str) -> str:
    return f"""
You are an AI assistant for an e-commerce store.

Event: {event}
Details: {details}

Respond with a helpful business-friendly suggestion.
"""
