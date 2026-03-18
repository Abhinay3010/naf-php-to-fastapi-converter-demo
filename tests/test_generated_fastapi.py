import os
import sys
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text

# Ensure repo root is in path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# ✅ Setup in-memory SQLite for testing (thread-safe)
engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False}
)

# ✅ Pre-create required tables (IMPORTANT: use begin())
with engine.begin() as conn:
    conn.execute(text("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            name TEXT
        );
    """))
    conn.execute(text("""
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            user_id INTEGER
        );
    """))
    conn.execute(text("""
        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            product_name TEXT,
            price REAL
        );
    """))

    # ✅ Insert dummy data (prevents empty responses / edge cases)
    conn.execute(text("""
        INSERT INTO users (name) VALUES ('Alice')
    """))
    conn.execute(text("""
        INSERT INTO orders (user_id) VALUES (1)
    """))
    conn.execute(text("""
        INSERT INTO products (product_name, price)
        VALUES ('test product', 9.99)
    """))

# Collect all generated FastAPI files
generated_files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith(".py")]

@pytest.mark.parametrize("file_name", generated_files)
def test_fastapi_file_import(file_name):
    """
    Test that the generated FastAPI file can be imported
    and its /auto-endpoint works with dummy parameters.
    """
    module_path = os.path.join(OUTPUT_DIR, file_name)
    module_name = file_name.replace(".py", "")
    
    import importlib.util
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Patch engine to use test in-memory DB
    module.engine = engine

    # Check app object exists
    assert hasattr(module, "app"), f"'app' not found in {file_name}"

    client = TestClient(module.app)

    # Detect required query params from function signature
    from inspect import signature
    sig = signature(module.auto_endpoint)
    params = {
        p.name: "test" if p.annotation == str else 1
        for p in sig.parameters.values()
    }

    # Call endpoint with dummy parameters
    response = client.get("/auto-endpoint", params=params)
    
    # Assert it works
    assert response.status_code == 200, f"{file_name} endpoint /auto-endpoint failed"
    assert isinstance(response.json(), list), f"{file_name} response is not a list"
