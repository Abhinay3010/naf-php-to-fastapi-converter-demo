import re

def extract_sql_queries(php_code: str) -> list[str]:
    """
    Extracts SQL queries from PHP code.
    Looks for $sql = "..." patterns.
    """
    return re.findall(r'\$sql\s*=\s*"([^"]+)"', php_code)

def extract_variables(php_code: str) -> list[str]:
    """
    Extracts PHP variable names used in the SQL query.
    E.g., $id, $name → ['id', 'name']
    """
    return re.findall(r'\$([a-zA-Z_][a-zA-Z0-9_]*)', php_code)
