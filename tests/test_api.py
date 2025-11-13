import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from fastapi.testclient import TestClient
from main import app
import io

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_list_files():
    response = client.get("/files")
    assert response.status_code == 200
    data = response.json()
    assert "files" in data
    assert isinstance(data["files"], list)


def test_upload_file():
    file_content = b"hello world"
    files = {"file": ("testfile.txt", io.BytesIO(file_content), "text/plain")}
    response = client.post("/files", files=files)
    assert response.status_code in (200, 201)

def test_get_uploaded_file():
    response = client.get("/files/testfile.txt")
    assert response.status_code == 200
    assert b"hello" in response.content

def test_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "files_stored_total" in data
