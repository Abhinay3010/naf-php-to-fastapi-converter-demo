import os
import sys
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from your_app.models import Base  # SQLAlchemy models

# Ensure repo root is in path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

OUTPUT_DIR = os.path.join(BASE_DIR, "output")
generated_files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith(".py")]

# Create in-memory DB
engine = create_engine("sqlite:///:memory:")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

@pytest.mark.parametrize("file_name", generated_files)
def test_fastapi_file_import(file_name):
    module_path = os.path.join(OUTPUT_DIR, file_name)
    module_name = file_name.replace(".py", "")
    
    import importlib.util
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    assert hasattr(module, "app"), f"'app' not found in {file_name}"

    client = TestClient(module.app)

    # Example payloads for endpoints (you may need to adjust per file)
    test_payloads = {
        "update_user_query1.py": {"id": 1, "name": "Alice"},
        "delete_user_query1.py": {"id": 1},
        "user_query1.py": {"name": "Bob"},
        "orders_query1.py": {"order_id": 1, "product_id": 1},
        "products_query1.py": {"product_name": "Widget", "price": 9.99},
    }

    payload = test_payloads.get(file_name, {})

    # Use POST/PUT/DELETE if payload exists, otherwise GET
    if payload:
        response = client.post("/auto-endpoint", json=payload)
    else:
        response = client.get("/auto-endpoint")

    assert response.status_code == 200, f"{file_name} endpoint /auto-endpoint failed"
