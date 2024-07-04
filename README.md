docker-compose up --build
cd frontend
python -m http.server 8080

curl.exe -X GET "http://localhost:8000/stocks/?symbol=AAPL&start_date=2000-01-01"



# Sistema de Sugestão de Investimentos

Este projeto implementa um sistema de sugestão de investimentos utilizando machine learning e análise de sentimento em notícias. A arquitetura é baseada em microserviços, desenvolvida em Python com FastAPI e PostgreSQL.

![Diagrama de Microservicos](images/DiagramaMicroservicos.jpg)

## Sumário

- [Estrutura de Microserviços](#estrutura-de-microserviços)
  - [API Gateway](#api-gateway)
  - [User Service](#user-service)
  - [Portfolio Service](#portfolio-service)
  - [News Fetcher Service](#news-fetcher-service)
  - [Sentiment Analysis Service](#sentiment-analysis-service)
  - [ML Prediction Service](#ml-prediction-service)
  - [Stock Fetcher Service](#stock-fetcher-service)
- [Extra](#Extra)

## Estrutura de Microserviços

1. **API Gateway**
2. **User Service**
3. **Portfolio Service**
4. **News Fetcher Service**
5. **Sentiment Analysis Service**
6. **ML Prediction Service**
7. **Stock Fetcher Service**

## API Gateway
### **Descrição**: Centraliza as requisições dos clientes e distribui para os microserviços.
### **Endpoints**: Todos os endpoints dos microserviços.

## User Service
### **Descrição**: Gerencia as informações dos usuários e o login.
### **Endpoints Iniciais**:
  - `POST /register`: Registrar um novo usuário.
  - `POST /login`: Autenticar um usuário.
  - `GET /profile`: Obter informações do perfil do usuário.
### **Banco de Dados**: PostgreSQL

## Portfolio Service
### **Descrição**: Armazena e gerencia informações sobre as ações do cliente.
### **Endpoints Iniciais**:
  - `POST /portfolio`: Criar um novo portfólio.
  - `GET /portfolio`: Obter o portfólio do usuário.
  - `PUT /portfolio`: Atualizar o portfólio do usuário.
### **Banco de Dados**: PostgreSQL

## News Fetcher Service
### **Descrição**: Centraliza a obtenção de dados por API (notícias e ações).
### **Endpoints Iniciais**:
  - `GET /news`: Obter as últimas notícias.
### **Banco de Dados**: SQL ou NoSQL

## Sentiment Analysis Service
### **Descrição**: Análise de sentimento em notícias utilizando deep learning.
### **Endpoints Iniciais**:
  - `POST /analyze`: Analisar o sentimento de uma notícia.
### **Banco de Dados**: SQL ou NoSQL
### **Tecnologias**: TensorFlow/PyTorch

## ML Prediction Service
### **Descrição**: Previsão de ações utilizando machine learning.
### **Endpoints Iniciais**:
  - `POST /predict`: Obter previsão de ações baseadas em notícias.
### **Banco de Dados**: PostgreSQL
### **Tecnologias**: scikit-learn

## Stock Fetcher Service
### **Descrição**: Obtém e gerencia dados de ações.
### **Endpoints Iniciais**:
  - `GET /stocks`: Obter informações sobre ações.
  - `POST /stocks`: Adicionar novas informações sobre ações.
### **Banco de Dados**: PostgreSQL

#### Justificativa da Escolha do PostgreSQL

Para este projeto, que envolve o armazenamento de dados históricos de ações de várias empresas, a escolha do banco de dados é crucial. Optamos por PostgreSQL em vez de uma solução NoSQL, levando em consideração os seguintes requisitos específicos do nosso projeto:

**Requisitos do Projeto:**
1. **Armazenamento de Dados Históricos:** Precisamos armazenar dados como data, abertura, fechamento, mínima, máxima e volume para várias empresas, com cada tabela armazenando informações individuais.
2. **Desempenho Rápido de Leitura:** Necessitamos de leituras rápidas entre datas específicas para alimentar gráficos dinâmicos em um site web.
3. **Treinamento de Modelos de Machine Learning:** O banco de dados será acessado diariamente para treinar modelos de machine learning, requerendo consistência e desempenho confiáveis.
4. **Escalabilidade Futura:** Pretendemos escalar para incluir mais empresas e potencialmente adicionar novas métricas no futuro.

**Por que PostgreSQL?**

1. **Desempenho Rápido de Leitura:**
   - PostgreSQL oferece suporte avançado a índices, o que nos permite criar índices eficientes em campos de data. Isso resulta em consultas rápidas, essencial para gerar gráficos dinâmicos que mostram o desempenho das ações ao longo do tempo.

2. **Consistência e Confiabilidade:**
   - Precisamos de consistência nos dados, especialmente para o treinamento de modelos de machine learning. PostgreSQL garante essa consistência através de suas transações ACID, assegurando que os dados estejam sempre corretos e atualizados.

3. **Consultas Complexas e Agregações:**
   - Nossa aplicação exige a execução de consultas complexas para análises detalhadas e relatórios. PostgreSQL permite realizar essas consultas de forma eficiente, facilitando o processamento e a visualização dos dados históricos.

4. **Ferramentas de Administração e Manutenção:**
   - PostgreSQL possui ferramentas robustas para backup, replicação e manutenção, garantindo que nossos dados estejam seguros e que o banco de dados seja fácil de gerenciar.

5. **Flexibilidade para Escalabilidade:**
   - Embora SQL tradicionalmente escale verticalmente, PostgreSQL oferece soluções para escalabilidade horizontal, o que nos permitirá crescer e incluir mais empresas e métricas conforme necessário.




## Extra


arrumar id company
```bash
docker-compose up --build

curl.exe -X POST "http://localhost:8000/stock-fetcher-service/add_company/?company_symbol=AAPL"

curl.exe -X GET "http://localhost:8000/stock-fetcher-service/stock-data/?company_id=1&start_date=2023-01-01&end_date=2023-12-31"

curl.exe -X GET "http://localhost:8000/stock-fetcher-service/ml-stock-data/?company_id=1"

```



