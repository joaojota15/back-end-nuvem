API GameConnect
Esta é a API para o GameConnect, uma plataforma que integra autenticação de e-mail/senha com login social via Steam, e inclui postagens de usuários.

🚀 Rodando com Docker (Método Recomendado)
Este método é o mais simples para rodar o projeto. Ele gerencia a API e o banco de dados PostgreSQL automaticamente.

Pré-requisitos
Git

Docker Desktop

1. Clonar o Repositório
Bash

git clone https://github.com/Mvlimaa/api_game_connect
cd api_game_connect

2. Criar o Arquivo .env
O Docker precisa das suas chaves secretas para rodar a aplicação. Copie o arquivo de exemplo:

Bash

cp .env.example .env
Agora, edite o arquivo .env e preencha as seguintes chaves:

SECRET_KEY: (Obrigatório) Uma chave secreta longa e aleatória para os tokens JWT.

STEAM_API_KEY: (Obrigatório) Sua chave da API da Steam.

SENDGRID_API_KEY: (Obrigatório) Sua chave do SendGrid para envio de e-mails.

MAIL_FROM: (Obrigatório) O e-mail verificado que você usa no SendGrid.

FRONTEND_URL: (Obrigatório) A URL do seu frontend (ex: http://localhost:3000).

Atenção: Você não precisa se preocupar com a DATABASE_URL no .env para o Docker, pois o docker-compose.yml gerencia a conexão com o banco de dados interno.

3. Construir e Rodar os Containers
No terminal, na raiz do projeto, execute:

Bash

docker-compose up --build
--build: Constrói a imagem da API pela primeira vez.

up: Inicia os containers da api e do db em conjunto.

4. Acessar a Aplicação
API (Swagger Docs): http://localhost:8000/docs

Banco de Dados (externo): Você pode se conectar ao banco PostgreSQL através do localhost:5432 com as credenciais do docker-compose.yml.

🛠️ Instalação Manual (Desenvolvimento)
Use este método se você preferir gerenciar o Python e o PostgreSQL manualmente na sua máquina.

Pré-requisitos
Git

Python 3.11

PostgreSQL (instalado, rodando e com um banco de dados gameconnect criado)

1. Clonar e Criar o Ambiente Virtual
Bash

git clone https://github.com/Mvlimaa/api_game_connect
cd api_game_connect

# Criar o ambiente virtual
python -m venv venv

# Ativar (Windows)
.\venv\Scripts\activate
# Ativar (Mac/Linux)
source venv/bin/activate
2. Instalar Dependências
Bash

pip install -r requirements.txt
3. Configurar o .env
Este passo é crucial para o modo manual.

Bash

cp .env.example .env
Edite o arquivo .env e preencha TODAS as chaves:

DATABASE_URL: (Obrigatório) A URL de conexão do seu banco PostgreSQL local (ex: postgresql://postgres:12345@localhost:5432/gameconnect).

SECRET_KEY

STEAM_API_KEY

SENDGRID_API_KEY

MAIL_FROM

FRONTEND_URL

4. Rodar a API
Com o ambiente virtual ativado e o .env configurado, rode o Uvicorn:

Bash

uvicorn app.main:app --reload
--reload: O servidor reinicia automaticamente quando você salva um arquivo.

5. Acessar a Aplicação
API (Swagger Docs): http://localhost:8000/docs

O que cada método faz
Docker: Cria ambientes "empacotados" chamados containers. O docker-compose.yml que criamos define dois pacotes: sua api (construída a partir do Dockerfile) e um db (usando uma imagem pronta do Postgres). Ele os conecta e garante que sua API sempre rode no mesmo ambiente, não importa a máquina.

Manual: É o jeito tradicional. Depende que a máquina tenha o Python, o Postgres e todas as bibliotecas (requirements.txt) instaladas corretamente, o que pode variar entre sistemas operacionais.