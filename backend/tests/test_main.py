from unittest.mock import patch

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_search():
    response = client.get("/api/search?query=test")
    assert response.status_code == 200


@patch("api.router.extract_entities_and_events")
def test_process_file(mock_extract):
    mock_extract.return_value = {"executive_summary": "Test summary"}

    file_content = b"This is a test case."
    response = client.post(
        "/api/process",
        data={"model": "qwen2.5:3b"},
        files={"file": ("test.txt", file_content, "text/plain")},
    )

    assert response.status_code == 200
    assert "structured_intelligence" in response.json()
