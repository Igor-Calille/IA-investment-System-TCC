docker-compose up --build
cd frontend
python -m http.server 8080

curl.exe -X GET "http://localhost:8000/stocks/?symbol=AAPL&start_date=2000-01-01"



# Sistema de Sugestão de Investimentos

Este projeto implementa um sistema de sugestão de investimentos utilizando machine learning e análise de sentimento em notícias. A arquitetura é baseada em microserviços, desenvolvida em Python com FastAPI e PostgreSQL.

![Diagrama de Microservicos](images/DiagramaMicroservicos.jpg)

## Estrutura de Microserviços

1. **User Service**
2. **Portfolio Service**
3. **News Fetcher Service**
4. **Sentiment Analysis Service**
5. **ML Prediction Service**
6. **Stock Fetcher Service**
7. **API Gateway**

### Requisitos Funcionais

#### API Gateway
- **Descrição**: Centraliza as requisições dos clientes e distribui para os microserviços.
- **Endpoints**: Todos os endpoints dos microserviços.

#### User Service
- **Descrição**: Gerencia as informações dos usuários e o login.
- **Endpoints Iniciais**:
  - `POST /register`: Registrar um novo usuário.
  - `POST /login`: Autenticar um usuário.
  - `GET /profile`: Obter informações do perfil do usuário.
- **Banco de Dados**: PostgreSQL

#### Portfolio Service
- **Descrição**: Armazena e gerencia informações sobre as ações do cliente.
- **Endpoints Iniciais**:
  - `POST /portfolio`: Criar um novo portfólio.
  - `GET /portfolio`: Obter o portfólio do usuário.
  - `PUT /portfolio`: Atualizar o portfólio do usuário.
- **Banco de Dados**: PostgreSQL

#### News Fetcher Service
- **Descrição**: Centraliza a obtenção de dados por API (notícias e ações).
- **Endpoints Iniciais**:
  - `GET /news`: Obter as últimas notícias.
- **Banco de Dados**: SQL ou NoSQL

#### Sentiment Analysis Service
- **Descrição**: Análise de sentimento em notícias utilizando deep learning.
- **Endpoints Iniciais**:
  - `POST /analyze`: Analisar o sentimento de uma notícia.
- **Banco de Dados**: SQL ou NoSQL
- **Tecnologias**: TensorFlow/PyTorch

#### ML Prediction Service
- **Descrição**: Previsão de ações utilizando machine learning.
- **Endpoints Iniciais**:
  - `POST /predict`: Obter previsão de ações baseadas em notícias.
- **Banco de Dados**: PostgreSQL
- **Tecnologias**: scikit-learn

#### Stock Fetcher Service
- **Descrição**: Obtém e gerencia dados de ações.
- **Endpoints Iniciais**:
  - `GET /stocks`: Obter informações sobre ações.
  - `POST /stocks`: Adicionar novas informações sobre ações.
- **Banco de Dados**: PostgreSQL

