import os
import sys
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add repo root and output folder to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
sys.path.append(BASE_DIR)
sys.path.append(OUTPUT_DIR)

# Import your SQLAlchemy Base
# Adjust this import depending on where your Base is defined
# For example, if you have output/db.py with Base:
from db import Base  

# Create an in-memory SQLite database
engine = create_engine("sqlite:///:memory:")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables before tests
Base.metadata.create_all(bind=engine)

# Collect all generated FastAPI files
generated_files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith(".py")]

# Minimal payloads for different generated files
# Add entries here for each generated endpoint that requires input
TEST_PAYLOADS = {
    "update_user_query1.py": {"id": 1, "name": "Alice"},
    "delete_user_query1.py": {"id": 1},
    "user_query1.py": {"name": "Bob"},
    "orders_query1.py": {"order_id": 1, "product_id": 1},
    "products_query1.py": {"product_name": "Widget", "price": 9.99},
    "sample1_query1.py": {"sample_field": "value"},  # adjust if needed
}

@pytest.mark.parametrize("file_name", generated_files)
def test_fastapi_file_import(file_name):
    """
    Test that each generated FastAPI file can be imported,
    has an 'app' object, and that /auto-endpoint works.
    """
    module_path = os.path.join(OUTPUT_DIR, file_name)
    module_name = file_name.replace(".py", "")
    
    import importlib.util
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    assert hasattr(module, "app"), f"'app' not found in {file_name}"

    client = TestClient(module.app)

    payload = TEST_PAYLOADS.get(file_name, {})

    # Use POST if payload exists, otherwise GET
    if payload:
        response = client.post("/auto-endpoint", json=payload)
    else:
        response = client.get("/auto-endpoint")

    assert response.status_code == 200, f"{file_name} endpoint /auto-endpoint failed"
