import re

def extract_sql_queries(php_code: str):
    """
    Extract SQL queries from PHP code.
    Looks for simple patterns like:
    - $sql = "SELECT ...";
    - $query = "UPDATE ...";
    Returns a list of SQL strings.
    """
    # Match $variable = "SQL ..."; or $variable = 'SQL ...';
    pattern = re.compile(
        r'\$\w+\s*=\s*(?P<quote>["\'])(.*?)\1\s*;', re.DOTALL
    )
    queries = []
    for match in pattern.finditer(php_code):
        sql_candidate = match.group(2).strip()
        # Simple heuristic: must contain SELECT, INSERT, UPDATE, or DELETE
        if re.search(r'\b(SELECT|INSERT|UPDATE|DELETE)\b', sql_candidate, re.IGNORECASE):
            queries.append(sql_candidate)
    return queries

def extract_variables(php_code: str):
    """
    Extract PHP variables that may be used in SQL queries.
    Returns a list of variable names without the $ sign.
    Example: $id, $name -> ['id', 'name']
    """
    return list(set(re.findall(r'\$([a-zA-Z_]\w*)', php_code)))
