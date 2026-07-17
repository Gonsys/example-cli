"""Serviço de tempo — lógica de negócio para obtenção do horário atual."""

import re
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

TIMEZONE_PATTERN = re.compile(r'^[A-Za-z0-9_/\-]{1,64}$')
DEFAULT_TIMEZONE = "America/Sao_Paulo"


class InvalidTimezoneError(Exception):
    """Exceção levantada quando uma zona horária inválida é informada."""

    def __init__(self, timezone: str):
        self.timezone = timezone
        self.message = f"Zona horária inválida: '{timezone}'"
        super().__init__(self.message)


def validate_timezone(timezone_str: str) -> str:
    """
    Valida o formato e existência da zona horária.

    Primeiro verifica se o formato atende ao regex (letras, números, _, /, -,
    máximo 64 caracteres). Em seguida, verifica se o identificador existe na
    base IANA via zoneinfo.ZoneInfo.

    Args:
        timezone_str: Identificador IANA da zona horária.

    Returns:
        A string da timezone validada.

    Raises:
        InvalidTimezoneError: se o formato for inválido ou a timezone não existir.
    """
    if not TIMEZONE_PATTERN.match(timezone_str):
        raise InvalidTimezoneError(timezone_str)

    try:
        ZoneInfo(timezone_str)
    except (ZoneInfoNotFoundError, KeyError):
        raise InvalidTimezoneError(timezone_str)

    return timezone_str


def get_current_time(timezone_str: str) -> dict:
    """
    Retorna a hora atual para a zona horária informada.

    Se timezone_str for vazio ou falsy, usa "America/Sao_Paulo" como padrão.

    Args:
        timezone_str: Identificador IANA (ex: "America/Sao_Paulo").
                      Se vazio, usa DEFAULT_TIMEZONE.

    Returns:
        dict com campos:
            - datetime: string ISO 8601 com precisão de segundos e offset
            - timezone: identificador IANA utilizado
            - utc_offset: offset no formato ±HH:MM

    Raises:
        InvalidTimezoneError: se a zona horária não for válida.
    """
    if not timezone_str:
        timezone_str = DEFAULT_TIMEZONE

    validate_timezone(timezone_str)

    tz = ZoneInfo(timezone_str)
    now = datetime.now(tz)

    # Formatar datetime em ISO 8601 com precisão de segundos (sem microsegundos)
    dt_formatted = now.replace(microsecond=0).isoformat()

    # Formatar utc_offset no formato ±HH:MM
    # strftime('%z') retorna algo como "+0530" ou "-0300"
    raw_offset = now.strftime('%z')
    utc_offset = f"{raw_offset[:3]}:{raw_offset[3:]}"

    return {
        "datetime": dt_formatted,
        "timezone": timezone_str,
        "utc_offset": utc_offset,
    }
