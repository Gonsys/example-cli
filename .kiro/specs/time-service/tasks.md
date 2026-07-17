# Implementation Plan: time-service

## Overview

Implementação incremental do serviço de consulta de horário com FastAPI, seguindo a estrutura de diretórios definida no design. Cada tarefa constrói sobre a anterior, começando pela estrutura do projeto e finalizando com a integração Docker.

## Tasks

- [x] 1. Configurar estrutura do projeto e dependências
  - [x] 1.1 Criar `pyproject.toml` com metadados e dependências
    - Criar o arquivo `pyproject.toml` na raiz do projeto com as dependências: fastapi, uvicorn, pydantic
    - Incluir grupo `[dev]` com: pytest, hypothesis, httpx, pytest-cov
    - Configurar metadados do projeto (nome, versão, descrição)
    - Configurar `requires-python = ">=3.14"`
    - _Requirements: 5.1, 5.3_

  - [x] 1.2 Criar estrutura de diretórios e arquivos `__init__.py`
    - Criar os diretórios: `app/`, `app/routers/`, `app/schemas/`, `app/services/`, `tests/`
    - Criar arquivos `__init__.py` vazios em cada pacote Python
    - _Requirements: 5.1_

- [x] 2. Implementar modelos e serviço de tempo
  - [x] 2.1 Criar schemas Pydantic (`app/schemas/time.py`)
    - Implementar `TimeResponse` com campos: `datetime` (str), `timezone` (str), `utc_offset` (str)
    - Implementar `ErrorResponse` com campo: `detail` (str)
    - _Requirements: 4.2, 4.3, 4.4, 4.5, 4.6_

  - [x] 2.2 Implementar serviço de tempo (`app/services/time.py`)
    - Implementar exceção `InvalidTimezoneError` com mensagem incluindo o valor inválido
    - Implementar `validate_timezone()` com regex `^[A-Za-z0-9_/\-]{1,64}$` e verificação via `zoneinfo.ZoneInfo`
    - Implementar `get_current_time(timezone_str)` que retorna dict com `datetime`, `timezone`, `utc_offset`
    - Usar `zoneinfo` (stdlib) para manipulação de fusos horários
    - Aplicar padrão "America/Sao_Paulo" quando timezone vazio ou omitido
    - Formatar datetime em ISO 8601 com precisão de segundos (sem microsegundos) e offset
    - Formatar utc_offset no formato ±HH:MM
    - _Requirements: 1.1, 1.2, 2.1, 2.2, 3.1, 3.2, 3.3_

  - [ ]* 2.3 Escrever teste de propriedade para timezone válida
    - **Property 1: Timezone válida produz resposta estruturada correta**
    - Usar estratégia `st.sampled_from(available_timezones())` do Hypothesis
    - Verificar que a resposta contém exatamente 3 campos com formatos corretos (ISO 8601, IANA, ±HH:MM)
    - Configurar `@settings(max_examples=100)`
    - **Validates: Requirements 1.1, 1.2, 4.2, 4.3, 4.4, 4.6**

  - [ ]* 2.4 Escrever teste de propriedade para timezone inválida
    - **Property 2: Timezone inválida produz erro com valor informado**
    - Usar estratégia `st.text()` filtrada para excluir timezones IANA válidas, combinada com `st.text(min_size=65)` para strings longas
    - Verificar status 400 e campo `detail` contendo o valor inválido
    - Configurar `@settings(max_examples=100)`
    - **Validates: Requirements 3.1, 3.2, 3.3, 4.5**

  - [ ]* 2.5 Escrever teste de propriedade para consistência utc_offset/datetime
    - **Property 3: Consistência entre utc_offset e datetime**
    - Usar estratégia `st.sampled_from(available_timezones())`
    - Verificar que `utc_offset` é idêntico aos últimos 6 caracteres do campo `datetime`
    - Configurar `@settings(max_examples=100)`
    - **Validates: Requirements 1.2, 4.2, 4.4**

- [x] 3. Implementar roteador e aplicação FastAPI
  - [x] 3.1 Criar roteador de tempo (`app/routers/time.py`)
    - Implementar endpoint `GET /time` com query parameter `timezone` (default vazio)
    - Chamar `get_current_time()` do serviço
    - Retornar `TimeResponse` em caso de sucesso (HTTP 200)
    - Tratar `InvalidTimezoneError` retornando HTTP 400 com `ErrorResponse`
    - _Requirements: 1.1, 2.1, 2.2, 3.1, 3.2_

  - [x] 3.2 Criar módulo principal (`app/main.py`)
    - Instanciar `FastAPI` com title, description e version
    - Registrar o roteador de tempo
    - Registrar exception handler para `InvalidTimezoneError`
    - _Requirements: 5.1, 6.1, 6.2, 6.3_

  - [ ]* 3.3 Escrever testes unitários do endpoint
    - Testar GET /time sem timezone → retorna America/Sao_Paulo (HTTP 200)
    - Testar GET /time?timezone= (vazio) → retorna America/Sao_Paulo (HTTP 200)
    - Testar GET /time?timezone=US/Eastern → retorna timezone correta (HTTP 200)
    - Testar GET /time?timezone=Invalid/Zone → retorna HTTP 400 com detail
    - Testar GET /time?timezone=<65+ chars> → retorna HTTP 400
    - Testar Content-Type application/json nas respostas
    - Testar que resposta de sucesso contém exatamente 3 campos
    - Usar `httpx.AsyncClient` com `TestClient` do FastAPI
    - _Requirements: 1.1, 2.1, 2.2, 3.1, 3.2, 3.3, 4.1, 4.6_

- [x] 4. Checkpoint — Verificação intermediária
  - Ensure all tests pass, ask the user if questions arise.

- [x] 5. Implementar documentação automática e Docker
  - [x] 5.1 Verificar documentação automática da API
    - Confirmar que GET /docs retorna Swagger UI (HTML, status 200)
    - Confirmar que GET /openapi.json retorna schema OpenAPI válido com descrição do endpoint /time
    - A documentação é gerada automaticamente pelo FastAPI — apenas verificar que está funcional
    - _Requirements: 6.1, 6.2, 6.3_

  - [x] 5.2 Criar Dockerfile
    - Usar imagem base Python slim compatível com 3.14
    - Instalar uv no container
    - Copiar pyproject.toml e instalar dependências com uv
    - Copiar código da aplicação
    - Expor porta 8000
    - Comando de entrada: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
    - _Requirements: 5.2, 5.3, 5.4_

  - [ ]* 5.3 Escrever testes unitários de documentação e startup
    - Testar que GET /docs retorna status 200 e content-type text/html
    - Testar que GET /openapi.json retorna status 200 e contém path "/time"
    - Testar que resposta padrão é retornada em tempo aceitável (< 500ms)
    - _Requirements: 6.1, 6.2, 6.3, 2.3_

- [x] 6. Checkpoint final — Validação completa
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tarefas marcadas com `*` são opcionais e podem ser ignoradas para um MVP mais rápido
- Cada tarefa referencia requisitos específicos para rastreabilidade
- Checkpoints garantem validação incremental
- Testes de propriedade (Hypothesis) validam propriedades universais de corretude
- Testes unitários (pytest) validam exemplos específicos e casos de borda
- Ambiente: Windows CMD — usar `uv run pytest tests/ -v` para executar testes
- Criar venv com: `uv venv --python 3.14t`
- Instalar dependências com: `uv pip install -e ".[dev]"`

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1", "1.2"] },
    { "id": 1, "tasks": ["2.1", "2.2"] },
    { "id": 2, "tasks": ["2.3", "2.4", "2.5", "3.1"] },
    { "id": 3, "tasks": ["3.2"] },
    { "id": 4, "tasks": ["3.3", "5.1", "5.2"] },
    { "id": 5, "tasks": ["5.3"] }
  ]
}
```
