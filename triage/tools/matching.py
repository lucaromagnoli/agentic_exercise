def match_query(query: str, log_line: str) -> bool:
    return all(x.lower() in log_line.lower()  for x in query.split())