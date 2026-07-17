# Requirements Document

## Introduction

Serviço de consulta de horário atual construído com Python e FastAPI. O serviço expõe um único endpoint `GET /time` que retorna a hora atual em uma zona horária especificada via query parameter. Caso nenhuma zona horária seja informada, o serviço assume o horário do Brasil (America/Sao_Paulo, UTC-3). O serviço deve ser executável tanto localmente quanto em container Docker.

## Glossary

- **Serviço_de_Hora**: Aplicação FastAPI que fornece o endpoint de consulta de horário
- **Endpoint_Time**: Rota HTTP GET `/time` que retorna a hora atual
- **Zona_Horária**: Identificador de fuso horário no formato IANA (ex: "America/Sao_Paulo", "US/Eastern")
- **Zona_Padrão**: Zona horária padrão utilizada quando nenhuma é especificada — definida como "America/Sao_Paulo" (UTC-3)
- **Resposta_de_Hora**: Objeto JSON contendo a hora atual formatada e metadados da zona horária

## Requirements

### Requirement 1: Consulta de horário com zona horária especificada

**User Story:** Como um consumidor da API, eu quero consultar a hora atual em uma zona horária específica, para que eu possa saber o horário em qualquer localidade do mundo.

#### Acceptance Criteria

1. WHEN uma requisição GET é recebida em `/time` com o query parameter `timezone` preenchido com um identificador IANA válido, THE Serviço_de_Hora SHALL retornar um objeto JSON contendo a hora atual naquela zona horária com precisão de segundos e status HTTP 200
2. THE Resposta_de_Hora SHALL conter os campos: `datetime` (data e hora no formato ISO 8601 com precisão de segundos, incluindo offset), `timezone` (identificador IANA da zona horária utilizada) e `utc_offset` (offset em relação ao UTC no formato ±HH:MM)

### Requirement 2: Zona horária padrão Brasil

**User Story:** Como um consumidor da API, eu quero que a hora do Brasil (UTC-3) seja retornada por padrão, para que eu não precise informar a zona horária toda vez que precisar do horário brasileiro.

#### Acceptance Criteria

1. WHEN uma requisição GET é recebida em `/time` sem o query parameter `timezone`, THE Serviço_de_Hora SHALL retornar a data e hora atual utilizando "America/Sao_Paulo" como zona horária padrão, com o campo `timezone` na resposta indicando "America/Sao_Paulo"
2. WHEN uma requisição GET é recebida em `/time` com o query parameter `timezone` vazio (e.g., `?timezone=`), THE Serviço_de_Hora SHALL retornar a data e hora atual utilizando "America/Sao_Paulo" como zona horária padrão, com o campo `timezone` na resposta indicando "America/Sao_Paulo"
3. WHEN uma requisição GET é recebida em `/time` sem o query parameter `timezone`, THE Serviço_de_Hora SHALL retornar a resposta em no máximo 500 milissegundos

### Requirement 3: Validação de zona horária inválida

**User Story:** Como um consumidor da API, eu quero receber uma mensagem de erro clara quando informo uma zona horária inválida, para que eu possa corrigir minha requisição.

#### Acceptance Criteria

1. IF o query parameter `timezone` contém um valor que não corresponde a nenhum identificador presente na base de dados IANA (formato "Area/Local", por exemplo "America/Sao_Paulo"), THEN THE Serviço_de_Hora SHALL retornar status HTTP 400 com um corpo JSON contendo o campo `detail`
2. WHEN o Serviço_de_Hora retorna status HTTP 400 por zona horária inválida, THE Resposta_de_Hora de erro SHALL conter o campo `detail` com uma mensagem indicando que a zona horária informada é inválida, incluindo o valor recebido no parâmetro
3. IF o query parameter `timezone` contém caracteres que não são compatíveis com o formato de identificador IANA (máximo de 64 caracteres, apenas letras, números, underscores, hífens e barras), THEN THE Serviço_de_Hora SHALL retornar status HTTP 400 com um corpo JSON contendo o campo `detail` indicando que a zona horária informada é inválida

### Requirement 4: Formato da resposta JSON

**User Story:** Como um consumidor da API, eu quero receber a resposta em formato JSON estruturado, para que eu possa integrar facilmente com outras aplicações.

#### Acceptance Criteria

1. THE Serviço_de_Hora SHALL retornar todas as respostas com Content-Type `application/json` e charset UTF-8
2. THE Resposta_de_Hora de sucesso SHALL conter o campo `datetime` no formato ISO 8601 (ex: "2024-01-15T14:30:00-03:00"), incluindo data, hora com precisão de segundos e offset UTC
3. THE Resposta_de_Hora de sucesso SHALL conter o campo `timezone` com o identificador IANA da zona horária utilizada (ex: "America/Sao_Paulo")
4. THE Resposta_de_Hora de sucesso SHALL conter o campo `utc_offset` como string representando o offset no formato ±HH:MM (ex: "-03:00")
5. IF uma requisição resultar em erro, THEN THE Serviço_de_Hora SHALL retornar uma resposta JSON contendo o campo `detail` com uma mensagem indicando o motivo do erro
6. THE Resposta_de_Hora de sucesso SHALL conter exclusivamente os campos `datetime`, `timezone` e `utc_offset`, sem campos adicionais

### Requirement 5: Execução local e em Docker

**User Story:** Como um desenvolvedor, eu quero executar o serviço tanto localmente quanto em container Docker, para que eu tenha flexibilidade no ambiente de execução.

#### Acceptance Criteria

1. WHEN o desenvolvedor executar o comando `uv run uvicorn app.main:app` ou ativar o venv e executar `uvicorn app.main:app`, THE Serviço_de_Hora SHALL iniciar e responder a requisições HTTP na porta 8000 em no máximo 10 segundos
2. THE Serviço_de_Hora SHALL incluir um Dockerfile que, ao ser construído com `docker build` e executado com `docker run`, resulte no serviço respondendo a requisições HTTP na porta 8000 do host em no máximo 30 segundos
3. THE Serviço_de_Hora SHALL escutar na porta 8000 por padrão em ambos os modos de execução (local e Docker)
4. WHEN executado em Docker, THE Serviço_de_Hora SHALL mapear a porta 8000 do container para a porta 8000 do host
5. IF a porta 8000 estiver indisponível no momento da inicialização, THEN THE Serviço_de_Hora SHALL falhar com uma mensagem de erro indicando que a porta está em uso

### Requirement 6: Documentação automática da API

**User Story:** Como um consumidor da API, eu quero acessar a documentação interativa, para que eu possa explorar e testar o endpoint facilmente.

#### Acceptance Criteria

1. WHEN um consumidor acessa o endpoint `/docs`, THE Serviço_de_Hora SHALL retornar uma página Swagger UI com status HTTP 200 e content-type `text/html`
2. WHEN um consumidor acessa o endpoint `/openapi.json`, THE Serviço_de_Hora SHALL retornar um documento OpenAPI válido com status HTTP 200 e content-type `application/json`
3. THE documentação OpenAPI SHALL incluir a descrição do endpoint `/time`, contendo método HTTP, formato de resposta e parâmetros disponíveis
