import os

# Estrutura de pastas e arquivos
structure = {
    "adapters": {
        "http": {
            "__init__.py": "",
            "routes.py": "# Definições das rotas da API\n",
            "schemas.py": "# Schemas de entrada e saída (Pydantic)\n"
        },
        "database": {
            "__init__.py": "",
            "models.py": "# Modelos do banco de dados (SQLAlchemy)\n",
            "repository.py": "# Lógica de acesso a dados (repositório)\n",
            "migrations.py": "# Scripts de migração do banco de dados\n"
        },
        "logging": {
            "__init__.py": "",
            "logger.py": "# Configuração do logger\n"
        }
    },
    "core": {
        "__init__.py": "",
        "config.py": "# Configurações gerais (ex: env vars)\n",
        "exceptions.py": "# Definições de exceções personalizadas\n",
        "constants.py": "# Constantes da aplicação\n"
    },
    "domain": {
        "__init__.py": "",
        "models.py": "# Entidades do domínio (Conta, Transacao)\n",
        "services.py": "# Lógica de negócios (serviços do domínio)\n",
        "value_objects.py": "# Objetos de valor\n"
    },
    "main.py": "# Ponto de entrada da aplicação\n"
}

def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)  # Recursão para subpastas
        else:
            with open(path, 'w') as file:
                file.write(content)

# Caminho para a pasta já existente "sistema_bancario"
base_path = "sistema_bancario"

# Cria a estrutura de pastas e arquivos dentro de "sistema_bancario"
create_structure(base_path, structure)
print("Estrutura de pastas e arquivos criada com sucesso dentro de 'sistema_bancario'!")
