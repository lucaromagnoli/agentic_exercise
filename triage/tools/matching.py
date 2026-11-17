def match_query(query: str, log_line: str) -> bool:
    terms = query.split()
    if terms:
        return all(term.lower() in log_line.lower() for term in terms)
    return False
