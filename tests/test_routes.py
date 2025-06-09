import os
import io
import pytest
from flask import Flask
from flask_app.web.routes import main
from unittest.mock import patch


@pytest.fixture
def client():
    app = Flask(__name__, template_folder=os.path.abspath("flask_app/templates"))
    app.config["TESTING"] = True
    app.register_blueprint(main)
    return app.test_client()


def test_upload_parses_and_runs_llm(client):
    with patch(
        "flask_app.web.routes.analyze_requirement", return_value="🧪 Mocked analysis"
    ), patch(
        "flask_app.web.routes.suggest_tests", return_value="🧪 Mocked test suggestion"
    ):
        data = {
            "srs_file": (
                io.BytesIO(b"# Test Section\nREQ-1 The system shall power on."),
                "test.txt",
            )
        }

        response = client.post("/upload", data=data, content_type="multipart/form-data")

        assert response.status_code == 200
        assert b"Test Section" in response.data
        assert b"REQ-1" in response.data
        assert b"Mocked analysis" in response.data
        assert b"Mocked test suggestion" in response.data
