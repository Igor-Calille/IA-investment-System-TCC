import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import pandas as pd
import json

class NLPModel():
    def __init__(self):


        model_name = 'mrm8488/deberta-v3-ft-financial-news-sentiment-analysis'
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        #self.model = AutoModelForSequenceClassification.from_pretrained("backtest\\scripts\\maket_sentiment\\results_model_english/_model")

    def market_trend(self, data):


        dataframe = pd.json_normalize(data)
        dataframe.set_index('date', inplace=True)

        dataframe.drop(columns=['img', 'link', 'media', 'reporter', 'site'], inplace=True)

        print(dataframe[0:3])

        """
        # Garantir que a coluna 'Data' esteja no formato datetime
        dataframe['Data'] = pd.to_datetime(dataframe['Data'])

        # Agrupar por data
        grouped = dataframe.groupby('Data')

        # Lista para armazenar data e sentimento médio
        date_sentiment_list = []

        for date, group in grouped:
            sentiments = []
            for index, row in group.iterrows():
                predicted_class = self.use_nlp_model(row['text'])
                sentiments.append(predicted_class)
            # Calcular sentimento médio para esta data
            average_sentiment = sum(sentiments) / len(sentiments)
            date_sentiment_list.append({'Data': date.date(), 'Sentimento': average_sentiment})

        # Criar um DataFrame a partir da lista
        output_df = pd.DataFrame(date_sentiment_list)

        """

        return dataframe

    def use_nlp_model(self, input_text):
        inputs = self.tokenizer(input_text, return_tensors='pt', truncation=True, padding=True).to(self.device)

        self.model.to(self.device)
        
        with torch.no_grad():
            outputs = self.model(**inputs)

        logits = outputs.logits
        predicted_class = torch.argmax(logits, dim=1).item()

        return predicted_class

