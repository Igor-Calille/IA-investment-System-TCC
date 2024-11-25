import React, { useState, useEffect } from 'react';
import { requisicoes_enviadas, requisicoes_finalizadas } from '../components/StockContext';

const TradeDecisionBox = ({ stock }) => {
    const [decision, setDecision] = useState("Carregando...");
    const [date, setDate] = useState("");
    const [predictedPrice, setPredictedPrice] = useState(0);
    const [actualPrice, setActualPrice] = useState(0);
    const [priceDifference, setPriceDifference] = useState(null);

  useEffect(() => {
    const fetchTradeDecision = async () => {
      try {
        // const url2 = `http://localhost:8000/stock-fetcher-service/add_company/?company_symbol=${stock}`;
        // if (!(requisicoes_enviadas.includes(stock) || requisicoes_finalizadas.includes(stock))) {
        //   try {
        //     requisicoes_enviadas.push(stock);
            
        //     const response = await fetch(url2, {
        //       method: 'POST', // Define o método como POST
        //       headers: {
        //         'Content-Type': 'application/json', // Define o tipo de conteúdo como JSON
        //       },
        //       body: JSON.stringify({}), // Corpo da requisição (adicione dados aqui se necessário)
        //     });
        //     if (!response.ok) {
        //       throw new Error('Erro na requisição');
        //     }
        //     const result = await response.json();

        //     requisicoes_finalizadas.push(stock);

        //   } catch (error) {
        //     console.error('Erro ao buscar os dados:', error);
        //   }
        // }

        while (!requisicoes_finalizadas.includes(stock)) {
          await new Promise((resolve) => setTimeout(resolve, 1000));
        }

        const response = await fetch(
          `http://localhost:8000/ml-prediction-service/train_model/?company_symbol=${stock}&start_date="2024-06-02"&end_date="2024-12-31"`
        );
        if (!response.ok) {
          throw new Error("Erro na requisição");
        }
        const result = await response.json();
        const lastData = result.data[result.data.length - 1]; // Último dado

        // Calcula a diferença percentual entre o preço real e o previsto
        const difference =
          ((lastData.predicted_close - lastData.close) / lastData.close) * 100;

        // Atualiza os estados com os dados recebidos
        setDecision(lastData.signal_ml === 1 ? "Comprar" : "Não Comprar");
        setDate(lastData.date);
        setPredictedPrice(lastData.predicted_close);
        setActualPrice(lastData.close);
        setPriceDifference(difference);
      } catch (error) {
        console.error("Erro ao buscar decisão de compra:", error);
        setDecision("Erro ao carregar dados");
      }
    };

    fetchTradeDecision();
  }, [stock]);

  return (
    <div className="trade-decision-box-parent">
    <div className="trade-decision-box">
      <h3>Decisão de Compra</h3>
      <p>
        <strong> {
            (decision === 'Comprar') ? 
              <span style={{color: 'green'}}>{decision}</span> : 
              <span style={{color: 'red'}}>{decision}</span>
        }
        </strong>
      </p>
      <p>
        <strong></strong> {date ? new Date(date).toLocaleDateString('pt-BR') : 'Carregando...'}
      </p>
      <p>
        <strong>Previsão:</strong> {predictedPrice ? `R$ ${predictedPrice.toFixed(2)}` : 'Carregando...'}
        <strong>
        {priceDifference !== null ? ` ${priceDifference.toFixed(2)}%` : " Carregando..."}
        </strong>
      </p>
    </div>
    </div>
  );
};

export default TradeDecisionBox;