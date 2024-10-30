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

