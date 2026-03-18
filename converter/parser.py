import re

def extract_sql_queries(php_code: str):
    """
    Extracts SQL queries from PHP code.
    Handles:
    - $query = "..."
    - $sql = '...'
    - multi-line queries
    Returns a list of SQL strings
    """
    # Match anything like $var = "SQL ..." or 'SQL ...';
    pattern = re.compile(
        r'\$\w+\s*=\s*(?P<quote>["\'])(.*?)\1;', 
        re.DOTALL | re.IGNORECASE
    )
    matches = pattern.findall(php_code)
    queries = []

    for quote, sql in matches:
        sql_clean = sql.strip()
        # Basic heuristic: must contain SELECT, INSERT, UPDATE, DELETE
        if re.search(r'\b(SELECT|INSERT|UPDATE|DELETE)\b', sql_clean, re.IGNORECASE):
            queries.append(sql_clean)

    return queries
