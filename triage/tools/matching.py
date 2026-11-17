def match_query(query: str, log_line: str) -> bool:
    stripped_query = query.strip()
    if stripped_query:
        return all(x.lower() in log_line.lower()  for x in stripped_query.split())
    return False
