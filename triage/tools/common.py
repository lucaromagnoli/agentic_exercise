from typing import Any


def match_query(query: str, text: str) -> bool:
    terms = query.split()
    if terms:
        return all(term.lower() in text.lower() for term in terms)
    return False


def common_error(
    message: str = "query must contain at least one term",
) -> dict[str, Any]:
    return {"error": message}
