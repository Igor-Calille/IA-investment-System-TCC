import json
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import TimeSeriesSplit, GridSearchCV

from app.services.IndicadoresMercado import Indicadores

class Model:
    def __init__(self) -> None:
        pass

    async def train_model(self, json_data):
        # Converte JSON para DataFrame
        data_pd = pd.DataFrame(json_data)
        
        # Processamento e Feature Engineering
        data_pd['date'] = pd.to_datetime(data_pd['date'])
        data_pd['target'] = data_pd['close'].shift(-1)

        features = ['open', 'high', 'low', 'close', 'volume']

        # Calcula os indicadores técnicos
        indicadores = Indicadores()
        data_pd['RSI_14'] = indicadores.compute_RSI(data_pd['close'])
        data_pd['STOCH_RSI_14'] = indicadores.get_stochastic_rsi(data_pd['close'])
        data_pd['MACD'] = indicadores.compute_MACD(data_pd['close'])

        features.extend(['RSI_14', 'STOCH_RSI_14', 'MACD'])

        # Remove linhas com valores nulos
        data_pd.dropna(inplace=True)

        # Define variáveis independentes (X) e dependentes (y)
        X = data_pd[features]
        y = data_pd['target']

        # Configura a divisão do tempo e o modelo
        tscv = TimeSeriesSplit(n_splits=5)
        model = RandomForestRegressor()

        # Hiperparâmetros para Grid Search
        param_search = {
            'n_estimators': [50, 100],
            'max_features': ['sqrt', 'log2'],
            'max_depth': [10, 20],
            'min_samples_split': [2, 5],
            'min_samples_leaf': [1, 2],
            'bootstrap': [True, False]
        }

        # Realiza a busca pelos melhores parâmetros
        gsearch = GridSearchCV(estimator=model, cv=tscv, param_grid=param_search, scoring='neg_mean_squared_error', n_jobs=-1, verbose=2)
        gsearch.fit(X, y)
        best_model = gsearch.best_estimator_

        # Predições e sinal de compra/venda
        data_pd['predicted_close'] = best_model.predict(X)
        data_pd['signal_ml'] = np.where(data_pd['predicted_close'] > data_pd['close'], 1, -1)

        # Converte o DataFrame para uma lista de dicionários JSON-friendly
        result = data_pd.to_dict(orient='records')
        
        # Converte tipos numpy para tipos nativos
        for row in result:
            for key, value in row.items():
                if isinstance(value, (np.int64, np.float64)):
                    row[key] = value.item()

        return result
