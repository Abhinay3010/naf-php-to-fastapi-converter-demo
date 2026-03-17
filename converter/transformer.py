def normalize_query(query: str):
    # Replace PHP variables like '$name' → :name
    import re
    query = re.sub(r"\$(\w+)", r":\1", query)
    return query
