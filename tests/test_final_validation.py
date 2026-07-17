"""
Checkpoint final — Validação completa do time-service.

Verifica todos os cenários de aceitação do serviço usando httpx TestClient.
"""

import re

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestDefaultTimezone:
    """Requirement 2: Zona horária padrão Brasil."""

    def test_get_time_no_timezone_returns_sao_paulo(self):
        """GET /time sem timezone → America/Sao_Paulo."""
        response = client.get("/time")
        assert response.status_code == 200
        data = response.json()
        assert data["timezone"] == "America/Sao_Paulo"

    def test_get_time_empty_timezone_returns_sao_paulo(self):
        """GET /time?timezone= (vazio) → America/Sao_Paulo."""
        response = client.get("/time", params={"timezone": ""})
        assert response.status_code == 200
        data = response.json()
        assert data["timezone"] == "America/Sao_Paulo"


class TestValidTimezones:
    """Requirement 1: Consulta de horário com zona horária especificada."""

    def test_us_eastern(self):
        """GET /time?timezone=US/Eastern → 200, correct timezone."""
        response = client.get("/time", params={"timezone": "US/Eastern"})
        assert response.status_code == 200
        data = response.json()
        assert data["timezone"] == "US/Eastern"

    def test_europe_london(self):
        """GET /time?timezone=Europe/London → 200, correct timezone."""
        response = client.get("/time", params={"timezone": "Europe/London"})
        assert response.status_code == 200
        data = response.json()
        assert data["timezone"] == "Europe/London"


class TestInvalidTimezones:
    """Requirement 3: Validação de zona horária inválida."""

    def test_invalid_zone_returns_400(self):
        """GET /time?timezone=Invalid/Zone → 400 com detail."""
        response = client.get("/time", params={"timezone": "Invalid/Zone"})
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "Invalid/Zone" in data["detail"]

    def test_too_long_timezone_rejected_by_regex(self):
        """GET /time?timezone=<65+ chars> → 400, rejected by regex."""
        long_tz = "a" * 65
        response = client.get("/time", params={"timezone": long_tz})
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data


class TestResponseStructure:
    """Requirement 4: Formato da resposta JSON."""

    def test_success_response_has_exactly_3_fields(self):
        """Resposta de sucesso contém exatamente 3 campos."""
        response = client.get("/time")
        data = response.json()
        assert set(data.keys()) == {"datetime", "timezone", "utc_offset"}

    def test_datetime_iso8601_with_seconds_precision(self):
        """Campo datetime no formato ISO 8601 com precisão de segundos."""
        response = client.get("/time")
        data = response.json()
        # Regex: YYYY-MM-DDTHH:MM:SS±HH:MM
        pattern = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}$"
        assert re.match(pattern, data["datetime"]), (
            f"datetime '{data['datetime']}' does not match ISO 8601 with seconds precision"
        )

    def test_utc_offset_format(self):
        """Campo utc_offset no formato ±HH:MM."""
        response = client.get("/time")
        data = response.json()
        pattern = r"^[+-]\d{2}:\d{2}$"
        assert re.match(pattern, data["utc_offset"]), (
            f"utc_offset '{data['utc_offset']}' does not match ±HH:MM format"
        )

    def test_utc_offset_matches_datetime_offset(self):
        """utc_offset deve ser idêntico ao offset do campo datetime (últimos 6 chars)."""
        response = client.get("/time")
        data = response.json()
        datetime_offset = data["datetime"][-6:]
        assert data["utc_offset"] == datetime_offset, (
            f"utc_offset '{data['utc_offset']}' != datetime offset '{datetime_offset}'"
        )

    def test_content_type_is_json(self):
        """Content-Type é application/json para respostas da API."""
        response = client.get("/time")
        assert "application/json" in response.headers["content-type"]

    def test_error_content_type_is_json(self):
        """Content-Type é application/json para respostas de erro."""
        response = client.get("/time", params={"timezone": "Invalid/Zone"})
        assert "application/json" in response.headers["content-type"]


class TestDocumentation:
    """Requirement 6: Documentação automática da API."""

    def test_docs_returns_html(self):
        """GET /docs → 200, text/html."""
        response = client.get("/docs")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    def test_openapi_json_contains_time_path(self):
        """GET /openapi.json → 200, contains /time path."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        assert "application/json" in response.headers["content-type"]
        data = response.json()
        assert "/time" in data.get("paths", {}), (
            "OpenAPI schema does not contain /time path"
        )


class TestDockerfile:
    """Requirement 5: Verificação do Dockerfile."""

    def test_dockerfile_exists_and_has_correct_structure(self):
        """Dockerfile existe e contém elementos essenciais."""
        import os
        dockerfile_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "Dockerfile",
        )
        assert os.path.exists(dockerfile_path), "Dockerfile not found"

        with open(dockerfile_path, "r") as f:
            content = f.read()

        # Verificar elementos essenciais
        assert "FROM" in content, "Dockerfile missing FROM instruction"
        assert "EXPOSE 8000" in content, "Dockerfile missing EXPOSE 8000"
        assert "uvicorn" in content, "Dockerfile missing uvicorn command"
        assert "app.main:app" in content, "Dockerfile missing app.main:app reference"
        assert "0.0.0.0" in content, "Dockerfile missing 0.0.0.0 host binding"
        assert "COPY" in content, "Dockerfile missing COPY instructions"
        assert "WORKDIR" in content, "Dockerfile missing WORKDIR"
