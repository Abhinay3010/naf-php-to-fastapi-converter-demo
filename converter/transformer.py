import re

def normalize_query(query: str, variables: list[str] = None) -> str:
    """
    Converts PHP variables ($var) and '?' placeholders to SQLAlchemy named parameters (:var)
    """
    # Replace PHP $var with :var
    query = re.sub(r'\$([a-zA-Z_][a-zA-Z0-9_]*)', r':\1', query)

    # Replace plain ? with sequential named params if variables provided
    if variables:
        for v in variables:
            query = query.replace('?', f':{v}', 1)

    return query
