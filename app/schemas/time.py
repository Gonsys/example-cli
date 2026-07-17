from pydantic import BaseModel


class TimeResponse(BaseModel):
    """Resposta de sucesso com a hora atual na zona horária solicitada."""

    datetime: str    # ISO 8601 com offset (ex: "2024-01-15T14:30:00-03:00")
    timezone: str    # Identificador IANA (ex: "America/Sao_Paulo")
    utc_offset: str  # Formato ±HH:MM (ex: "-03:00")


class ErrorResponse(BaseModel):
    """Resposta de erro com mensagem descritiva."""

    detail: str      # Mensagem descritiva do erro
