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
### **Banco de Dados**: PostgreSQL
### **Tecnologias**:

**Requisitos do Microserviço:**

## Portfolio Service
### **Descrição**: Armazena e gerencia informações sobre as ações do cliente.
### **Endpoints Iniciais**:
### **Banco de Dados**: PostgreSQL
### **Tecnologias**:

**Requisitos do Microserviço:**

## News Fetcher Service
### **Descrição**: Centraliza a obtenção de dados por API (notícias e ações).
### **Endpoints Iniciais**:
### **Banco de Dados**: SQL ou NoSQL
### **Tecnologias**:

**Requisitos do Microserviço:**

## Sentiment Analysis Service
### **Descrição**: Análise de sentimento em notícias utilizando deep learning.
### **Endpoints Iniciais**:
  - `GET sentiment-analysis-service/analyze/`: Obter a análise de sentimento das notícia da empresa requisitada.
### **Banco de Dados**: SQL ou NoSQL
### **Tecnologias**: Python e PyTorch

**Requisitos do Microserviço:**

## ML Prediction Service
### **Descrição**: Previsão de ações utilizando machine learning.
### **Endpoints Iniciais**:
  - `GET /ml-prediction-service/predict/`: Obter previsão de ações sobre a empresa requisitada.
### **Banco de Dados**: PostgreSQL
### **Tecnologias**: Python, C++ e scikit-learn

**Requisitos do Microserviço:**
1. **Treinar diariamente um modelo de Machine Learning:**
2. **Fornecer previsão diarias:**

## Stock Fetcher Service
### **Descrição**: Obtém e gerencia dados de ações.
### **Endpoints Iniciais**:
  - `POST /stock-fetcher-service/add_company/`: Adicionar uma nova empresa no Banco de Dados.
  - `GET /stock-fetcher-service/stock-data/`: Obter dados de ações para gráficos dinâmicos.
  - `GET /stock-fetcher-service/ml-stock-data/`: Enviar dados das ações para treinamento de machine learning
### **Banco de Dados**: PostgreSQL
### **Tecnologias**: Python

**Requisitos do Microserviço:**
1. **Armazenamento de Dados Históricos:** Precisamos armazenar dados como data, abertura, fechamento, mínima, máxima e volume para várias empresas, com cada tabela armazenando informações individuais.
2. **Desempenho Rápido de Leitura:** Necessitamos de leituras rápidas entre datas específicas para alimentar gráficos dinâmicos em um site web.
3. **Treinamento de Modelos de Machine Learning:** O banco de dados será acessado diariamente para treinar modelos de machine learning, requerendo consistência e desempenho confiáveis.
4. **Escalabilidade Futura:** Pretendemos escalar para incluir mais empresas e potencialmente adicionar novas métricas no futuro.

#### Justificativa da Escolha do PostgreSQL

Para este projeto, que envolve o armazenamento de dados históricos de ações de várias empresas, a escolha do banco de dados é crucial. Optamos por PostgreSQL em vez de uma solução NoSQL, levando em consideração os seguintes requisitos não funcionais do nosso projeto:


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



