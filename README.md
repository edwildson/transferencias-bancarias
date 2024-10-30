# Sistema de Transações Bancárias

Este projeto é um sistema de transações bancárias desenvolvido em Python utilizando FastAPI para a criação da API e Kafka como sistema de mensageria para processamento assíncrono de eventos.

## Funcionalidades

- **Cadastro de Contas Bancárias**: Criação e gerenciamento de contas com saldo inicial.
- **Transações**: Permite realizar depósitos, saques e transferências entre contas.
- **Concorrência Segura**: Suporte a múltiplas transações simultâneas com garantia de integridade dos saldos.
- **Consumo Assíncrono de Eventos**: Processamento de eventos de transações a partir de um tópico Kafka.
- **Logs de Transações**: Registro de todas as operações realizadas para rastreamento e auditoria.


## Tecnologias Utilizadas

- **FastAPI**: Framework para construção de APIs assíncronas.
- **SQLAlchemy**: ORM para manipulação de banco de dados.
- **PostgreSQL**: Sistema de gerenciamento de banco de dados.
- **Kafka**: Sistema de mensageria para processamento assíncrono de eventos.
- **Pydantic**: Validação de dados e gerenciamento de configurações.

## Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/edwildson/transferencias-bancarias.git
   cd transferencias-bancarias

2. Suba os containers com docker compose up -d

3. Acesse http://localhost:8000/docs para ver a documentação da API

## CASOS 

1. Cadastro de Conta
Para criar uma nova conta, você pode usar o seguinte comando curl:
  ```bash
  curl -X POST "http://localhost:8000/contas" \
  -H "Content-Type: application/json" \
  -d '{"numero": 123, "saldo": 1000}'
  ```

2. Depósito em Conta
  Para realizar um depósito em uma conta, use:
  ```bash
  curl -X POST "http://localhost:8000/transacoes/deposito" \
  -H "Content-Type: application/json" \
  -d '{"conta": 123, "valor": 500}'
  ```

3. Saque de Conta
  Para sacar de uma conta, use:
  ```bash
  curl -X POST "http://localhost:8000/transacoes/saque" \
  -H "Content-Type: application/json" \
  -d '{"conta": 123, "valor": 200}'
  ```

4. Transferência entre Contas
  Para transferir dinheiro entre contas, use:
  ```bash
  curl -X POST "http://localhost:8000/transacoes/transferencia" \
  -H "Content-Type: application/json" \
  -d '{"conta_origem": 123, "conta_destino": 456, "valor": 300}'
  ```


## Cenários de Teste

#### Cenário 1: Concorrência em Saque
1. Criar Contas:
  Crie duas contas com os seguintes saldos:
  Conta 123: R$ 1000
  Conta 456: R$ 500

2. Realizar Saque Concorrente:
  Inicie dois processos de saque simultaneamente para a mesma conta (Conta 123) com o valor de R$ 800.
  ```bash
  curl -X POST "http://localhost:8000/transacoes/saque" \
  -H "Content-Type: application/json" \
  -d '{"conta": 123, "valor": 800}' &

  curl -X POST "http://localhost:8000/transacoes/saque" \
  -H "Content-Type: application/json" \
  -d '{"conta": 123, "valor": 800}' &
  ```

3. Verificar Saldo:
  Após a execução dos saques, verifique o saldo da Conta 123. O saldo não deve ser menor que zero e deve refletir apenas um saque.


#### Cenário 2: Concorrência em Transferências
1. Criar Contas:
  Crie duas contas:
  Conta 123: R$ 1000
  Conta 456: R$ 500

2. Realizar Transferências Concorrentes:
  Inicie dois processos de transferência simultânea:
  Transferir R$ 300 da Conta 123 para a Conta 456.
  Transferir R$ 200 da Conta 123 para a Conta 456.

  ```bash
  curl -X POST "http://localhost:8000/transacoes/transferencia" \
  -H "Content-Type: application/json" \
  -d '{"conta_origem": 123, "conta_destino": 456, "valor": 300}' &

  curl -X POST "http://localhost:8000/transacoes/transferencia" \
  -H "Content-Type: application/json" \
  -d '{"conta_origem": 123, "conta_destino": 456, "valor": 200}' &
  ```

3. Verificar Saldos:
  Após a execução das transferências, verifique os saldos das contas:
  Conta 123 deve ter R$ 500 (R$ 1000 - R$ 300 - R$ 200).
  Conta 456 deve ter R$ 800 (R$ 500 + R$ 300 + R$ 200).

#### Cenário 3: Tratamento de Saldo Insuficiente
1. Criar Conta:
  Crie uma conta com saldo de R$ 100.
2. Saque com Saldo Insuficiente:
  Tente realizar um saque de R$ 200.
  ```bash
  Copiar código
  curl -X POST "http://localhost:8000/transacoes/saque" \
  -H "Content-Type: application/json" \
  -d '{"conta": 123, "valor": 200}'
  ```

3. Verificar Erro:
  O sistema deve retornar um erro indicando que o saldo é insuficiente para realizar o saque.
