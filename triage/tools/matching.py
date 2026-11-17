def match_query(query: str, text: str) -> bool:
    terms = query.split()
    if terms:
        return all(term.lower() in text.lower() for term in terms)
    return False
