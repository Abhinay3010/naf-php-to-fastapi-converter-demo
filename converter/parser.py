import re

def extract_sql_queries(php_code: str):
    pattern = r'query\("(.+?)"\)'
    return re.findall(pattern, php_code)

def extract_variables(php_code: str):
    pattern = r"\$_GET\['(.+?)'\]"
    return re.findall(pattern, php_code)
