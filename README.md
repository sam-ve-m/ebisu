# Ebisu
#### _API para consulta de dados dos clientes._
___
## Iniciando o projeto
### Passo 1
#### Criação do ambiente
Crie e inicie um virtual env para o projeto. 

- Para criar o ambiente virtual execute:
```bash
python3 -m venv env
```
- Para realizar a ativação execute:

    No Linux:
    ```bash
    source env/bin/activate
    ```
    No Windows:
    ```shell
    env\Scripts\activate.bat
    ```

### Passo 2
#### Instalação de dependências
1. __Instalar os pacotes no virtual env a partir do seguinte comando:__
    
    ```bash
    pip install -r requirements.txt --extra-index-url "https://nexus.sigame.com.br/repository/pypi/simple/"
    ```  
    O comando pedirá um usuário e senha, preencha-os e os pacotes serão instalados.


2. __Instalar as bibliotecas do Cliente Oracle no computador, para poder acessar o banco de dados.__
    
    Os arquivos de download estão disponíveis a partir desse link:
    ```
    https://www.oracle.com/database/technologies/instant-client.html
    ```
| __Observação:__ no caso de sistemas Ubuntu é recomendado fazer o download do arquivo `.rpm` e fazer a conversão para `.deb`. |
|------------------------------------------------------------------------------------------------------------------------------|

### Passo 3
#### Criação das variáveis de ambiente
É necessário criar as variáveis de ambiente do projeto e de duas dependências do projeto: `heimdall-client` e `mist-client`. 

1. Crie um arquivo `.env` no caminho `/opt/envs/ebisu.lionx.com.br/`, seguindo esse modelo:

~~~bash
# oracle orders
ORACLE_USER_ORDERS=FILL_THIS_WITH_VALUE
ORACLE_PASSWORD_ORDERS=FILL_THIS_WITH_VALUE
ORACLE_BASE_DSN_ORDERS=FILL_THIS_WITH_VALUE
ORACLE_PORT_ORDERS=FILL_THIS_WITH_VALUE
ORACLE_SERVICE_US=FILL_THIS_WITH_VALUE
ORACLE_SERVICE_BR=FILL_THIS_WITH_VALUE

# mongodb user bank account
MONGO_CONNECTION_URL=FILL_THIS_WITH_VALUE
MONGODB_DATABASE_NAME=FILL_THIS_WITH_VALUE
MONGODB_USER_COLLECTION=FILL_THIS_WITH_VALUE
MONGODB_JWT_COLLECTION=FILL_THIS_WITH_VALUE

# oracle statement
ORACLE_BASE_DSN_STATEMENT=FILL_THIS_WITH_VALUE
ORACLE_USER_STATEMENT=FILL_THIS_WITH_VALUE
ORACLE_PASSWORD_STATEMENT=FILL_THIS_WITH_VALUE
ORACLE_SERVICE_STATEMENT=FILL_THIS_WITH_VALUE
ORACLE_ENCODING_STATEMENT=FILL_THIS_WITH_VALUE
ORACLE_PORT_STATEMENT=FILL_THIS_WITH_VALUE

# oracle earning
ORACLE_BASE_DNS_EARNINGS=FILL_THIS_WITH_VALUE
ORACLE_PORT_EARNINGS=FILL_THIS_WITH_VALUE
ORACLE_SERVICE_EARNINGS=FILL_THIS_WITH_VALUE
ORACLE_ENCODING_STATEMENT=FILL_THIS_WITH_VALUE
ORACLE_USER_EARNINGS=FILL_THIS_WITH_VALUE
ORACLE_PASSWORD_EARNINGS=FILL_THIS_WITH_VALUE

# mongo general
MONGODB_USER=FILL_THIS_WITH_VALUE
MONGODB_PASSWORD=FILL_THIS_WITH_VALUE
MONGODB_HOST=FILL_THIS_WITH_VALUE
MONGODB_PORT=FILL_THIS_WITH_VALUE
MONGODB_CONNECTION=FILL_THIS_WITH_VALUE
MONGO_DATABASE_POSEIDON=FILL_THIS_WITH_VALUE
MONGO_COLLECTION_IZANAMI=FILL_THIS_WITH_VALUE

# DW
DW_APP_KEY=FILL_THIS_WITH_VALUE
DW_USER=FILL_THIS_WITH_VALUE
DW_PASSWORD=FILL_THIS_WITH_VALUE
DW_AUTHENTICATION_URL=FILL_THIS_WITH_VALUE
DW_BALANCE_URL=FILL_THIS_WITH_VALUE
DW_GET_ALL_TRANSACTIONS_URL=FILL_THIS_WITH_VALUE

# S3
AWS_ACCESS_KEY_ID=FILL_THIS_WITH_VALUE
AWS_SECRET_ACCESS_KEY=FILL_THIS_WITH_VALUE
REGION_NAME=FILL_THIS_WITH_VALUE
AWS_FILE_BUCKET_NAME=FILL_THIS_WITH_VALUE

# bucket
JWT_FILE_BUCKET_NAME=FILL_THIS_WITH_VALUE
BUCKET_NAME_KEY=FILL_THIS_WITH_VALUE

BANK_CODE=FILL_THIS_WITH_VALUE
~~~

2. Crie outro arquivo `.env` no caminho `/opt/envs/heimdall.lionx.com.br/`, seguindo esse modelo:

~~~bash
HEIMDALL_FILE_BUCKET_NAME=FILL_THIS_WITH_VALUE
HEIMDALL_AWS_ACCESS_KEY_ID=FILL_THIS_WITH_VALUE
HEIMDALL_AWS_SECRET_ACCESS_KEY=FILL_THIS_WITH_VALUE
HEIMDALL_REGION_NAME=FILL_THIS_WITH_VALUE
HEIMDALL_BUCKET_NAME_KEY=FILL_THIS_WITH_VALUE
HEIMDALL_AWS_BUCKET_USERS_FILES=FILL_THIS_WITH_VALUE
HEIMDALL_AWS_BUCKET_TERMS=FILL_THIS_WITH_VALUE
HEIMDALL_JWT_REQUIRED_FIELDS=FILL_THIS_WITH_VALUE
HEIMDALL_REDIS_HOST=FILL_THIS_WITH_VALUE
HEIMDALL_REDIS_PORT=FILL_THIS_WITH_VALUE
HEIMDALL_REDIS_DB=FILL_THIS_WITH_VALUE
HEIMDALL_REDIS_USER=FILL_THIS_WITH_VALUE
HEIMDALL_REDIS_PASSWORD=FILL_THIS_WITH_VALUE
~~~

3. Crie um último arquivo `.env` no caminho `/opt/envs/mist.lionx.com.br/`, seguindo esse modelo:

~~~bash
MIST_REDIS_HOST=FILL_THIS_WITH_VALUE
MIST_REDIS_PORT=FILL_THIS_WITH_VALUE
MIST_REDIS_DB=FILL_THIS_WITH_VALUE
MIST_REDIS_USER=FILL_THIS_WITH_VALUE
MIST_REDIS_PASSWORD=FILL_THIS_WITH_VALUE
MIST_AWS_ACCESS_KEY_ID=FILL_THIS_WITH_VALUE
MIST_AWS_SECRET_ACCESS_KEY=FILL_THIS_WITH_VALUE
MIST_REGION_NAME=FILL_THIS_WITH_VALUE
MIST_BUCKET_NAME_KEY=FILL_THIS_WITH_VALUE
MIST_JWT_FILE_BUCKET_NAME=FILL_THIS_WITH_VALUE
MIST_ELECTRONIC_SIGNATURE_FILE_BUCKET_NAME=FILL_THIS_WITH_VALUE
MIST_JWT_REQUIRED_FIELDS=FILL_THIS_WITH_VALUE
MIST_MONGODB_CONNECTION=FILL_THIS_WITH_VALUE
MIST_AUTH_DATABASE_NAME=FILL_THIS_WITH_VALUE
MIST_AUTH_DATABASE_USER_COLLECTION=FILL_THIS_WITH_VALUE
MIST_ELECTRONIC_SIGNATURE_MAX_ATTEMPTS=FILL_THIS_WITH_VALUE
MIST_ENCRYPT_KEY=FILL_THIS_WITH_VALUE
LOG_NAME=FILL_THIS_WITH_VALUE
~~~

### Passo 4
Rodar o arquivo `run.py` para iniciar o projeto.
___
## Endpoints
A API possui os seguintes endpoints, listados abaixo por tópicos:

### 1. Balance
### 1.1. `balance`
- Rota HTTP: `| GET | http://localhost:8000/balance`
> _Retorna o valor do saldo na conta do usuário._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro | Descrição                    |
|-----------|------------------------------|
| `region`  | Região do balanço (BR ou US) |
&nbsp; 

#### Modelo de requisição:
```http
http://0.0.0.0:8000/balance?region=BR
```

#### Modelo de resposta:

~~~json
{
    "payload": {
        "balance": 53552784.17
    }
}
~~~
&nbsp; 
### 2. Broker Note
### 2.1. `list_broker_note`
- Rota HTTP: `| GET | http://localhost:8000/list_broker_note`
> _Retorna as notas de corretagem de um cliente em determinado período._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro | Descrição                                                  |
|-----------|------------------------------------------------------------|
| `region`  | Região das notas (BR ou US).                               |
| `year`    | (OPCIONAL) Ano da consulta, na forma de um número inteiro. |
| `month`   | (OPCIONAL) Mês da consulta, na forma de um número inteiro. |
&nbsp; 

#### Modelo de requisição:
```http
http://0.0.0.0:8000/list_broker_note?region=BR&year=2022&month=3
```

#### Modelo de resposta:

~~~json
{
    "available": []
}
~~~
&nbsp; 

### 2.2. `broker_note_pdf`
- Rota HTTP: `| GET | http://localhost:8000/broker_note_pdf`
> _Retorna um link com o PDF da nota de corretagem._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro | Descrição                                                  |
|-----------|------------------------------------------------------------|
| `region`  | Região das notas (BR ou US).                               |
| `year`    | (OPCIONAL) Ano da consulta, na forma de um número inteiro. |
| `month`   | (OPCIONAL) Mês da consulta, na forma de um número inteiro. |
| `day`     | (OPCIONAL) Dia da consulta, na forma de um número inteiro. |
&nbsp; 

#### Modelo de requisição:
```http
http://0.0.0.0:8000/broker_note_pdf?year=2021&month=03&day=10&region=BR
```

#### Modelo de resposta:

~~~json
{
"pdf_link": "link do pdf"
}
~~~

&nbsp;

### 3. Bank Statement
### 3.1. `bank_statement`
- Rota HTTP: `| GET | http://localhost:8000/bank_statement`
> _Retorna o extrato bancário de um usuário._

&nbsp;
#### Parâmetros da requisição:
| Parâmetro    | Descrição                                                                                        |
|--------------|--------------------------------------------------------------------------------------------------|
| `region`     | Região das notas (BR ou US).                                                                     |
| `limit`      | O número de movimentações a serem retornadas, na forma de um número inteiro.                     |
| `offset`     | O número de páginas que serão exibidas, na forma de um número inteiro.                           |
| `start_date` | Data de início da consulta, no formato Unix Timestamp com a adição de três zeros ao final (000). |
| `end_date`   | Data de fim da consulta, no formato Unix Timestamp com a adição de três zeros ao final (000).    |
&nbsp;

#### Modelo de requisição:
```http
http://0.0.0.0:8000/bank_statement?region=BR&limit=2&offset=1&start_date=1646757399000&end_date=1648485399000
```

#### Modelo de resposta:

~~~json
{
  "balance": 53552784.17,
  "statements": [
    {
      "date": 1646794800.0,
      "description": "Comprovante de Bolsa para 09/03/2022 NC: 827   ",
      "value": -16523.96
    },
    {
      "date": 1646881200.0,
      "description": "Prévia Chamada de Margem Garantias de Operações",
      "value": -3163.0
    }
  ]
}
~~~

&nbsp;

### 3.2. `request_bank_statement_pdf`
- Rota HTTP: `| GET | http://localhost:8000/request_bank_statement_pdf`
> _Retorna o PDF do extrato bancário do usuário._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro    | Descrição                                                                                        |
|--------------|--------------------------------------------------------------------------------------------------|
| `region`     | Região das notas (BR ou US).                                                                     |

&nbsp; 

#### Modelo de requisição:
```http
http://0.0.0.0:8000/request_bank_statement_pdf?region=BR
```

&nbsp;


### 4. Client Orders
### 4.1. `client_orders`
- Rota HTTP: `| GET | http://localhost:8000/client_orders`

> _Retorna os dados de uma ordem de um cliente._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro     | Descrição                                      |
|---------------|------------------------------------------------|
| `region`      | Região das notas (BR ou US).                   |
| `cl_order_id` | ID da ordem de um cliente, na forma de string. |

&nbsp; 

#### Modelo de requisição:
```http
http://0.0.0.0:8000/client_orders?region=BR&cl_order_id=09c4432157ebe66ff9688fb8cd65726174fcdb18
```

#### Modelo de resposta:

~~~json
[
    {
        "cl_order_id": "008shs3-ee2a-4b08-b277-74b8b56f6e64",
        "account": "000000000-1",
        "time": 1644626388.0,
        "quantity": 100,
        "average_price": 0,
        "price": 0,
        "last_price": 0,
        "stop_price": 0,
        "currency": "BRL",
        "symbol": "VALE3",
        "side": "buy",
        "status": "REJECTED",
        "tif": "DAY",
        "total_spent": 0.0,
        "quantity_filled": 0.0,
        "quantity_leaves": 0,
        "quantity_last": 0,
        "text": "Please Contact Admin/Brokerage for Help -> Sem saldo para esta operacao.  Login: INTEGRALIONX. Vlr.Disp R$: -12.490.989,95. Vlr total da ordem R$: 9.600,00. Compras em aberto R$: 0,00",
        "reject_reason": 0,
        "exec_type": "REJECTED",
        "expire_date": null,
        "error_message": null
    }
]
~~~

&nbsp; 


### 4.2. `list_client_orders`
- Rota HTTP: `| GET | http://localhost:8000/list_client_orders`

> _Retorna uma lista com todas as ordens de um cliente._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro      | Descrição                                                                    |
|----------------|------------------------------------------------------------------------------|
| `region`       | Região das notas (BR ou US).                                                 |
| `limit`        | O número máximo de ordens a serem retornadas, na forma de um número inteiro. |
| `offset`       | O número de páginas que serão exibidas, na forma de um número inteiro.       |
| `order_status` | (OPCIONAL) O status das ordens a serem retornadas, na forma de string.       |

- __Observação__ 
  
  Os status de ordem disponíveis são:
  - NEW
  - PARTIALLY_FILLED
  - FILLED
  - DONE_FOR_DAY
  - CANCELED
  - REPLACED
  - PENDING_CANCEL
  - STOPPED
  - REJECTED
  - SUSPENDED
  - PENDING_NEW
  - CALCULATED
  - EXPIRED
  - ACCEPTED_FOR_BIDDING
  - PENDING_REPLACE
  - PREVIOUS_FINAL_STATE

&nbsp;

#### Modelo de requisição:
```http
http://0.0.0.0:8000/list_client_orders?region=BR&limit=3&offset=0
```

#### Modelo de resposta:

~~~json
[
    {
        "name": "Petroleo Brasileiro SA Petrobras",
        "cl_order_id": "7bd7dfg1-980f-4f94-a488-83108d5a6491",
        "time": 1649889704.0,
        "quantity": 100,
        "order_type": null,
        "average_price": 0,
        "currency": "BRL",
        "symbol": "PETR3",
        "status": "REJECTED",
        "total_spent": 0.0
    },
    {
        "name": "JBS SA",
        "cl_order_id": "554d1564-cfe0-4ad5-bd2c-22e5b42c65cd",
        "time": 1649886375.0,
        "quantity": 2000,
        "order_type": "LIMIT",
        "average_price": 38.01,
        "currency": "BRL",
        "symbol": "JBSS3",
        "status": "PARTIALLY_FILLED",
        "total_spent": 45612.0
    },
    {
        "name": "Petroleo Brasileiro SA Petrobras",
        "cl_order_id": "e677d189-9211-45fe-9c39-810d8efc4982",
        "time": 1649884700.0,
        "quantity": 1000,
        "order_type": "LIMIT",
        "average_price": 38.01,
        "currency": "BRL",
        "symbol": "PETR3",
        "status": "PARTIALLY_FILLED",
        "total_spent": 11403.0
    }
]
~~~

&nbsp; 


### 5. Earnings

### 5.1. `earnings`
- Rota HTTP: `| GET | http://localhost:8000/earnings`

> _Retorna os dividendos de um cliente em determinada ação._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro   | Descrição                                                                                 |
|-------------|-------------------------------------------------------------------------------------------|
| `symbol`    | O ticker que o cliente comprou (ex: JBSS3).                                               |
| `timestamp` | Data dos dividendos, no formato Unix Timestamp com a adição de três zeros ao final (000). |
| `limit`     | O número máximo de dividendos a serem retornados, na forma de um número inteiro.          |
| `offset`    | O número de páginas a serem exibidas, na forma de um número float.                        |
&nbsp; 

#### Modelo de requisição:
```http
http://0.0.0.0:8000/earnings?symbol=PETR4&timestamp=1617035799&offset=0&limit=1
```

&nbsp;  


### 6. User Bank Account
### 6.1. `list_bank_accounts`
- Rota HTTP: `| GET | http://localhost:8000/user/list_bank_accounts`

> _Retorna lista de contas bancárias de um usuário._

&nbsp; 
#### Parâmetros da requisição:
| (sem parâmetros) |
|------------------|


&nbsp; 

#### Modelo de requisição:
```http
http://0.0.0.0:8000/user/list_bank_accounts
```

#### Modelo de resposta:

~~~json
{
    "status_code": 200,
    "jwt_data": {
        "bank_accounts": [
            {
                "bank": "648498574893",
                "account_type": "1",
                "agency": "00987875",
                "account_number": "00056-3",
                "account_name": "corrente",
                "id": "0d27313f-5h32-477f-8a41-999dc4a301e0",
                "status": "active"
            },
            {
                "bank": "648498574893",
                "account_type": "2",
                "agency": "0087465",
                "account_number": "00000025-1",
                "account_name": "poupança",
                "id": "2f19b9ff-e123-4fb2-8819-4555cfc4d944",
                "status": "active"
            }
        ]
    }
}
~~~

&nbsp;  


### 6.2. `create_bank_account`
- Rota HTTP: `| POST | http://localhost:8000/user/create_bank_account`

> _Adiciona uma conta bancária para um usuário._

&nbsp; 
#### Parâmetros da requisição:
| (sem parâmetros) |
|------------------|


&nbsp; 

#### Modelo de requisição:
```http
http://0.0.0.0:8000/user/create_bank_account
```

#### Modelo do corpo da requisição:

~~~json
{
    "bank": "123",
    "account_type": "123",
    "agency": "001",
    "account_number": "000000000-1",
    "account_name": "poupança",
    "cpf":"12345678900"
}
~~~

&nbsp;   


### 6.3. `update_bank_account`
- Rota HTTP: `| PUT | http://localhost:8000/user/update_bank_account`

> _Atualiza uma conta bancária de um usuário._

&nbsp; 
#### Parâmetros da requisição:
| (sem parâmetros) |
|------------------|


&nbsp; 

#### Modelo de requisição:
```http
http://0.0.0.0:8000/user/update_bank_account
```

#### Modelo do corpo da requisição:

~~~json
{
    "bank": "123",
    "account_type": "123",
    "agency": "001",
    "account_number": "000000000-1",
    "account_name": "poupança",
    "cpf":"12345678900", 
    "id": "0d27313f-hgf3-477f-8a41-923dc4o301e0",
    "status": "active"
}
~~~

&nbsp;   


### 6.4. `delete_bank_account`
- Rota HTTP: `| DELETE | http://localhost:8000/user/delete_bank_account`

> _Deleta uma conta bancária de um usuário._

&nbsp; 
#### Parâmetros da requisição:
| (sem parâmetros) |
|------------------|


&nbsp; 

#### Modelo de requisição:
```http
http://0.0.0.0:8000/user/delete_bank_account
```

#### Modelo do corpo da requisição:

~~~json
{
    "id": "0d27313f-hgf3-477f-8a41-923dc4o301e0"
}
~~~

&nbsp; 


### 7. Bank Transfer
### 7.1. `transfer`
- Rota HTTP: `| GET | http://localhost:8000/transfer`

> _Retorna os dados necessários para a realização da transferência bancária (TED ou DOC): agência, conta e número do banco._

&nbsp; 
#### Parâmetros da requisição:
| (sem parâmetros) |
|------------------|


&nbsp; 

#### Modelo de requisição:
```http
http://0.0.0.0:8000/transfer
```

#### Modelo de resposta (DANDO ERRO):

~~~json
{
    "agency": "0001",
    "bank": "1212123",
    "account": "000000001-1"
}
~~~

&nbsp; 

---

## Erros e exceções
### BadRequestError
- **Código HTTP:** `400 Bad Request `
- Erro lançado quando o servidor não consegue processar a requisição por conta de um problema de sintaxe.

### UnauthorizedError
- **Código HTTP:** `401 Unauthorized`
- Erro lançado quando as credenciais de autenticação estão inválidas.

### IntegrityJwtError
- **Código HTTP:** `401 Unauthorized`
- Erro lançado quando as credenciais de autenticação estão inválidas.

### AuthenticationJwtError
- **Código HTTP:** `401 Unauthorized`
- Erro lançado quando as credenciais de autenticação estão inválidas.

### ForbiddenError
- **Código HTTP:** `403 Forbidden`
- Erro lançado quando o acesso é proibido.

### ForbiddenError
- **Código HTTP:** `403 Forbidden`
- Erro lançado quando o acesso é proibido.

### InternalServerError
- **Código HTTP:** `500 Internal Server Error`
- Erro lançado quando uma condição inesperada acontece no servidor.

### ExceptionError
- **Código HTTP:** `500 Internal Server Error`
- Erro lançado quando ocorre algum erro que não se encaixa nas condições listadas acima.

---
## Swagger
É possível ver as requisições pelo link abaixo após rodar o projeto, no entanto elas apresentarão erro por
não possuírem o token de autenticação JWT:
> http://0.0.0.0:8000/docs
>
> http://localhost:8000/docs

| Recomendado utilizar uma plataforma para testes de APIs, como o Postman. |
|--------------------------------------------------------------------------|