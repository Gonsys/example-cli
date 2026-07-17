"""Roteador de tempo — endpoint GET /time."""

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from app.schemas.time import ErrorResponse, TimeResponse
from app.services.time import InvalidTimezoneError, get_current_time

router = APIRouter()


@router.get(
    "/time",
    response_model=TimeResponse,
    responses={400: {"model": ErrorResponse}},
)
async def get_time(
    timezone: str = Query(default="", description="Zona horária IANA"),
):
    """Retorna a hora atual na zona horária informada (padrão: America/Sao_Paulo)."""
    try:
        result = get_current_time(timezone)
        return TimeResponse(**result)
    except InvalidTimezoneError as exc:
        return JSONResponse(
            status_code=400,
            content={"detail": exc.message},
        )
