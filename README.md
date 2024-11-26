# Sistema de Sugestão de Investimentos

O objetivo principal do projeto é auxiliar os investidores com uma ferramenta que utilize aprendizado de máquina e processamento de linguagem natural (NLP) para criar previsões precisas de preços e tendências sobre o mercado de ações.

![Diagrama de Microserviços](images/DiagramaMicroservicos.jpg)

## Sumário

- [Estrutura de Microserviços](#estrutura-de-microserviços)
  - [API Gateway](#api-gateway)
  - [News Fetcher Service](#news-fetcher-service)
  - [Sentiment Analysis Service](#sentiment-analysis-service)
  - [ML Prediction Service](#ml-prediction-service)
  - [Stock Fetcher Service](#stock-fetcher-service)
- [Como Executar](#Executar)

## Estrutura de Microserviços

1. **API Gateway**
2. **News Fetcher Service**
3. **Sentiment Analysis Service**
4. **ML Prediction Service**
5. **Stock Fetcher Service**

## API Gateway

### **Descrição**
Centraliza as requisições dos clientes, distribui para os microserviços e agrega respostas para facilitar o consumo pelo frontend.

### **Endpoints**
#### **Stock Fetcher Service**
- **Adicionar uma nova empresa ao banco de dados:**
  - `POST /stock-fetcher-service/add_company/`
  - Parâmetros:
    - `company_symbol` (string): Símbolo da empresa a ser adicionada.
  - Descrição: Envia uma requisição para adicionar uma nova empresa ao banco de dados.

- **Obter dados de ações para gráficos dinâmicos:**
  - `GET /stock-fetcher-service/stock-data/`
  - Parâmetros:
    - `company_symbol` (string): Símbolo da empresa.
    - `start_date` (string, opcional): Data inicial no formato `YYYY-MM-DD`.
    - `end_date` (string, opcional): Data final no formato `YYYY-MM-DD`.
  - Descrição: Retorna dados históricos de ações.

- **Obter dados para treinamento de Machine Learning:**
  - `GET /stock-fetcher-service/ml-stock-data/`
  - Parâmetros:
    - `company_symbol` (string): Símbolo da empresa.
  - Descrição: Retorna dados de ações formatados para treinamento de machine learning.

#### **ML Prediction Service**
- **Treinar o modelo de machine learning:**
  - `GET /ml-prediction-service/train_model/`
  - Parâmetros:
    - `company_symbol` (string): Símbolo da empresa.
    - `start_date` (string, opcional): Data inicial no formato `YYYY-MM-DD`.
    - `end_date` (string, opcional): Data final no formato `YYYY-MM-DD`.
  - Descrição: Dispara o treinamento do modelo e salva o resultado como JSON.

#### **News Fetcher Service**
- **Obter notícias de hoje:**
  - `GET /news-fetcher-service/news/today/`
  - Parâmetros:
    - `company` (string): Nome ou símbolo da empresa.
  - Descrição: Retorna notícias mais recentes de uma empresa no período de 24 horas.

- **Obter notícias em um intervalo de datas:**
  - `GET /news-fetcher-service/news/by_date/`
  - Parâmetros:
    - `company` (string): Nome ou símbolo da empresa.
    - `start_date` (string): Data inicial no formato `YYYY-MM-DD`.
    - `end_date` (string): Data final no formato `YYYY-MM-DD`.
  - Descrição: Retorna notícias de uma empresa em um intervalo de datas específico.

#### **Sentiment Analysis Service**
- **Obter a média de sentimento para notícias em um intervalo:**
  - `GET /sentiment-analysis-service/get_sentiment/`
  - Parâmetros:
    - `company_name` (string): Nome ou símbolo da empresa.
    - `start_date` (string, opcional): Data inicial no formato `YYYY-MM-DD`.
    - `end_date` (string, opcional): Data final no formato `YYYY-MM-DD`.
  - Descrição: Calcula o sentimento médio das notícias de uma empresa em um intervalo de datas.

- **Obter o sentimento de um texto específico:**
  - `GET /sentiment-analysis-service/get_sentiment_text/`
  - Parâmetros:
    - `text` (string): Texto para análise.
  - Descrição: Realiza a análise de sentimento em um texto fornecido.

### **Tecnologias**
- **Frameworks:** FastAPI
- **Middleware:** CORS configurado para permitir comunicação segura entre frontend e backend.
- **HTTP Client:** httpx para requisições assíncronas.

## News Fetcher Service

### **Descrição**
Centraliza a obtenção de dados por API, como notícias de empresas, para análise e consumo por outros microserviços.

### **Endpoints Atualizados**
- **Obter notícias de uma empresa no período de 24 horas:**
  - `GET /api/news/{company}/today`
  - Parâmetros:
    - `company` (string): Nome ou símbolo da empresa.
  - Descrição: Retorna notícias de uma empresa no período de 24 horas anteriores à data atual.

- **Obter notícias de uma empresa em um intervalo de datas:**
  - `GET /api/news/{company}`
  - Parâmetros:
    - `start` (string, obrigatório): Data inicial no formato `DD/MM/YYYY`.
    - `end` (string, obrigatório): Data final no formato `DD/MM/YYYY`.
    - `company` (string): Nome ou símbolo da empresa.
  - Descrição: Retorna notícias de uma empresa em um intervalo de datas fornecido.

### **Tecnologias**
- **Frameworks:** Flask
- **Middleware:** Flask-CORS para habilitar comunicações seguras entre diferentes origens.
- **Dependências Externas:** `fetch_news` para consumir APIs externas e obter notícias.

### **Requisitos do Microserviço**
- Conexão com APIs externas para buscar notícias relevantes de empresas específicas.
- Manipulação de intervalos de datas para busca personalizada.
- Tratamento robusto de erros e validação de parâmetros.

### **Exemplos de Erros e Tratamento**
- **Parâmetros ausentes ou inválidos:**
  - Resposta: `404 Not Found`
  - Causa: Faltam as datas `start` ou `end`, ou estas estão em formatos inválidos.
- **Erro no processamento das notícias:**
  - Resposta: `404 Not Found`
  - Causa: Problemas durante a manipulação ou transformação dos dados recebidos.

### **Notas Adicionais**
- Datas inválidas ou ausentes são tratadas para garantir a consistência da resposta.
- Campos com valores incorretos, como `datetime`, são ajustados para `None` para evitar inconsistências.

## Sentiment Analysis Service

### **Descrição**
Fornece análise de sentimento em notícias e textos utilizando modelos de deep learning, permitindo uma melhor compreensão do impacto emocional de eventos no mercado.

### **Endpoints Atualizados**
- **Obter análise de sentimento das notícias de uma empresa em um período:**
  - `GET /sentiment-analysis-service/get_sentiment/`
  - Parâmetros:
    - `company_name` (string, obrigatório): Nome ou símbolo da empresa.
    - `start_date` (string, opcional): Data inicial no formato `YYYY-MM-DD`.
    - `end_date` (string, opcional): Data final no formato `YYYY-MM-DD`.
  - Descrição: Retorna a análise de sentimento das notícias de uma empresa. Se as datas não forem especificadas, utiliza as notícias do dia atual.

- **Obter análise de sentimento de um texto específico:**
  - `GET /sentiment-analysis-service/get_sentiment_text/`
  - Parâmetros:
    - `text` (string, obrigatório): Texto para análise.
  - Descrição: Retorna o sentimento (positivo, negativo, neutro) de um texto fornecido.

### **Tecnologias**
- **Frameworks:** FastAPI para API robusta e escalável.
- **Deep Learning:** PyTorch para implementação de modelos de NLP.
- **HTTP Client:** httpx para comunicação assíncrona com o serviço de coleta de notícias.

### **Requisitos do Microserviço**
1. **Modelos de Deep Learning:**
   - Utilizar modelos avançados para detecção de sentimentos e tendências de mercado.
2. **Integração com News Fetcher Service:**
   - Consumir dados de notícias por meio de endpoints externos.
3. **Resultados em Tempo Real:**
   - Processar rapidamente grandes volumes de texto para gerar insights úteis.

### **Funcionalidades Adicionais**
- **Tratamento de Dados:**
  - Agregação de dados de notícias recebidas, transformando listas aninhadas em formatos planos para análise.
- **Manuseio de Erros:**
  - Timeout explícito com mensagens claras.
  - Detalhamento de erros para depuração eficaz.

### **Exemplo de Fluxo**
1. O cliente requisita a análise de sentimento das notícias de uma empresa.
2. O serviço consome dados do **News Fetcher Service**.
3. O modelo de NLP analisa as notícias e retorna a tendência de mercado.
4. O resultado é disponibilizado como uma resposta JSON detalhada.

### **Notas de Implementação**
- **Timeout Personalizado:** O timeout está configurado em 200 segundos para operações de rede, com mensagens claras em caso de falhas.
- **Flattening de Dados:** Notícias estruturadas em listas aninhadas são transformadas para garantir compatibilidade com o modelo de NLP.

### **Possíveis Melhorias Futuras**
- Adicionar suporte a análise de sentimentos para múltiplas empresas em uma única chamada.
- Implementar cache para respostas de análise de sentimento em notícias recorrentes.

## ML Prediction Service

### **Descrição**
Realiza previsões de ações utilizando modelos de machine learning, baseando-se em dados históricos e tendências de mercado.

### **Endpoints Atualizados**
- **Treinar o modelo de machine learning:**
  - `GET /ml-prediction-service/train_model/`
  - Parâmetros:
    - `company_symbol` (string, obrigatório): Símbolo da empresa.
    - `start_date` (string, opcional): Data inicial no formato `YYYY-MM-DD`.
    - `end_date` (string, opcional): Data final no formato `YYYY-MM-DD`.
  - Descrição: Treina o modelo de machine learning com os dados históricos da empresa fornecida.

### **Tecnologias**
- **Frameworks:** FastAPI para API eficiente e de alto desempenho.
- **Machine Learning:** scikit-learn para modelagem e treinamento de algoritmos.
- **HTTP Client:** httpx para comunicação assíncrona com o serviço de dados de ações.

### **Requisitos do Microserviço**
1. **Treinamento Diário:**
   - Realizar treinamento do modelo diariamente utilizando dados atualizados.
2. **Previsões Precisas:**
   - Garantir previsões com base em dados históricos obtidos do serviço **Stock Fetcher Service**.

### **Funcionalidades Adicionais**
- **Integração com Stock Fetcher Service:**
  - Busca os dados históricos necessários para treinamento.
- **Modelo Personalizado:**
  - Utiliza a classe `Model` para processar os dados e treinar o modelo.

### **Tratamento de Erros**
- **Timeout Personalizado:** 
  - O timeout está configurado para 200 segundos com mensagens detalhadas em caso de falha.
- **Manuseio de Respostas HTTP:**
  - Respostas com códigos de erro do **Stock Fetcher Service** resultam em mensagens claras para depuração.

### **Notas de Implementação**
- **Treinamento Customizado:**
  - O treinamento do modelo é iniciado diretamente após a obtenção dos dados de ações.
- **Formato da Resposta:**
  - Retorna o resultado do treinamento do modelo, permitindo que outros serviços consumam a saída.

### **Possíveis Melhorias Futuras**
- Adicionar suporte para múltiplos modelos e algoritmos, escolhendo o mais adequado automaticamente.
- Implementar armazenamento dos modelos treinados para previsões futuras.
- Adicionar métricas de desempenho como precisão e erro médio absoluto para avaliar a qualidade do modelo.

## Stock Fetcher Service

### **Descrição**
Obtém e gerencia dados de ações, fornecendo informações detalhadas e históricas para análises, gráficos e treinamento de modelos de machine learning.

### **Endpoints Atualizados**
- **Adicionar uma nova empresa ao banco de dados:**
  - `POST /stock-fetcher-service/add_company/`
  - Parâmetros:
    - `company_symbol` (string, obrigatório): Símbolo da empresa.
  - Descrição: Adiciona uma nova empresa ao banco de dados. Retorna um erro caso a empresa já exista.

- **Obter dados de ações para gráficos dinâmicos:**
  - `GET /stock-fetcher-service/stock-data/`
  - Parâmetros:
    - `symbol` (string, obrigatório): Símbolo da empresa.
    - `start_date` (string, opcional): Data inicial no formato `YYYY-MM-DD`.
    - `end_date` (string, opcional): Data final no formato `YYYY-MM-DD`.
  - Descrição: Retorna dados históricos de ações para uso em gráficos dinâmicos.

- **Obter dados de ações para treinamento de machine learning:**
  - `GET /stock-fetcher-service/ml-stock-data/`
  - Parâmetros:
    - `symbol` (string, obrigatório): Símbolo da empresa.
    - `start_date` (string, opcional): Data inicial no formato `YYYY-MM-DD`.
    - `end_date` (string, opcional): Data final no formato `YYYY-MM-DD`.
  - Descrição: Retorna dados históricos de ações formatados para uso em modelos de machine learning.

### **Banco de Dados**
- **PostgreSQL:** Utilizado para armazenar dados de empresas e ações, garantindo consistência e eficiência.

### **Tecnologias**
- **Frameworks:** FastAPI para desenvolvimento do backend.
- **Banco de Dados:** PostgreSQL para armazenamento robusto de dados históricos.
- **ORM:** SQLAlchemy para interagir com o banco de dados.
- **Agendador de Tarefas:** APScheduler para atualização automática de dados diários.
- **Middleware:** CORS configurado para permitir comunicação segura com o frontend.

### **Requisitos do Microserviço**
1. **Armazenamento de Dados Históricos:**
   - Dados como abertura, fechamento, mínima, máxima e volume.
2. **Desempenho Rápido de Leitura:**
   - Otimização para consultas rápidas com filtros por datas.
3. **Treinamento de Modelos:**
   - Acesso a dados históricos para alimentar modelos de machine learning.
4. **Atualização Automática:**
   - Tarefas diárias de atualização para o mercado brasileiro e americano.

### **Agendamento de Atualizações**
- **Mercado Brasileiro (B3):**
  - Horário: 18:00 (America/Sao_Paulo)
  - Descrição: Atualiza os dados das empresas brasileiras.
- **Mercado Americano (NYSE):**
  - Horário: 17:00 (America/New_York)
  - Descrição: Atualiza os dados das empresas americanas.

### **Tratamento de Erros**
- **Empresa já existente:**
  - Código de Resposta: 200
  - Mensagem: "Company already exists."
- **Dados de ações não encontrados:**
  - Código de Resposta: 404
  - Mensagem: "Data not found."
- **Erro de validação de parâmetros:**
  - Código de Resposta: 400
  - Mensagem: Detalhes do erro.

### **Notas de Implementação**
- **Manutenção de Tabelas:** O esquema do banco de dados é recriado automaticamente com base nos modelos definidos.
- **Escalabilidade:** Preparado para gerenciar um número crescente de empresas e métricas.
- **Integração com Outros Serviços:** Fornece dados para outros microserviços, como previsão de machine learning.

### **Possíveis Melhorias Futuras**
- Adicionar suporte a mercados adicionais (como Ásia e Europa).
- Implementar cache para consultas frequentes.
- Adicionar suporte a novos indicadores financeiros e métricas de mercado.


## Executar

### Guia de Execução do Sistema de Microserviços

Siga os passos abaixo para configurar e executar o sistema:

#### **1. Instalar o Docker**
Caso não tenha o Docker instalado, faça o download e instale-o a partir do link oficial:
- [Docker Download](https://www.docker.com/products/docker-desktop/)

#### **2. Abrir o Docker**
- Após a instalação, inicie o Docker Desktop. Certifique-se de que o Docker está em execução antes de continuar.

#### **3. Executar o Docker Compose**
- Navegue até o diretório raiz do projeto onde o arquivo `docker-compose.yml` está localizado.
- Abra um terminal e execute o comando abaixo para iniciar todos os serviços:
  ```bash
  docker-compose up --build
  ```

#### **4. Adicionar uma Empresa ao Banco de Dados**
- Abra um novo terminal para adicionar uma empresa ao banco de dados. Este passo é necessário para que os dados da empresa possam ser acessados no frontend.
- Use o seguinte comando `curl` para adicionar uma empresa, substituindo `AAPL` pelo símbolo da empresa desejada (no exemplo abaixo, estamos adicionando a Apple):
  ```bash
  curl.exe -X POST "http://localhost:8000/stock-fetcher-service/add_company/?company_symbol=AAPL"
  ```
- Certifique-se de que o comando foi executado com sucesso antes de prosseguir.

#### **5. Rodar o Frontend**
- Abra o navegador e acesse o seguinte endereço para visualizar o frontend:
  ```
  http://localhost:3000
  ```

Agora, o sistema está configurado e pronto para uso. Você pode interagir com o frontend e utilizar os serviços disponíveis.

