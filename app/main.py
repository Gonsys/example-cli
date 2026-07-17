"""Módulo principal — instância FastAPI e configuração da aplicação."""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.routers import time
from app.services.time import InvalidTimezoneError

app = FastAPI(
    title="Time Service",
    description="Serviço de consulta de horário atual com suporte a zonas horárias IANA",
    version="1.0.0",
)

app.include_router(time.router)


@app.exception_handler(InvalidTimezoneError)
async def invalid_timezone_handler(request: Request, exc: InvalidTimezoneError):
    """Handler global para exceções de timezone inválida."""
    return JSONResponse(
        status_code=400,
        content={"detail": exc.message},
    )
