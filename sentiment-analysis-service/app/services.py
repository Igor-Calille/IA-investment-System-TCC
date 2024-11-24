import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import pandas as pd
import json
import os

class NLPModel():
    def __init__(self):
        if torch.cuda.is_available():
            self.device = torch.device('cuda')
        else:
            self.device = torch.device('cpu')

        model_name = 'mrm8488/deberta-v3-ft-financial-news-sentiment-analysis'
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

        model_path = os.path.join("app", "results_model_portuguese", "_model")
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)

    def market_trend(self, data):
        # Criar DataFrame a partir dos dados
        dataframe = pd.DataFrame(data)

        # Adicionar um ano fictício às datas
        dataframe['date'] = dataframe['date'] + " 2024"

        # Converter a coluna 'date' para datetime com o ano adicionado
        dataframe['date'] = pd.to_datetime(dataframe['date'], format='%b %d %Y', errors='coerce')


        # Log: verificar o DataFrame após a conversão
        print("DataFrame após conversão de datas:", dataframe)

        # Agrupar por data
        grouped = dataframe.groupby('date')
        print("Agrupamento por data:", grouped)

        # Lista para armazenar data e sentimento médio
        date_sentiment_list = []

        for date, group in grouped:
            sentiments = []
            for index, row in group.iterrows():
                predicted_class = self.use_nlp_model(row['title'])
                sentiments.append(predicted_class)
            # Calcular sentimento médio para esta data
            average_sentiment = sum(sentiments) / len(sentiments)
            if average_sentiment > 1.5:
                sentiment_pred = "Muito positivo"
            elif average_sentiment > 1.0 and average_sentiment <= 1.5:
                sentiment_pred = "Positivo"
            elif average_sentiment == 1.0:
                sentiment_pred = "Neutro"
            elif average_sentiment > 0.5 and average_sentiment < 1.0:
                sentiment_pred = "Negativo"
            else:
                sentiment_pred = "Muito negativo"

            date_sentiment_list.append({'date': date.date(), 'sentiment_num': average_sentiment, 'sentiment_pred': sentiment_pred})

        return date_sentiment_list
    
    def get_text_sentiment(self, text:str):
        predicted_class = self.use_nlp_model(text)
        if predicted_class > 1.5:
            sentiment_pred = "Muito positivo"
        elif predicted_class > 1.0 and predicted_class <= 1.5:
            sentiment_pred = "Positivo"
        elif predicted_class == 1.0:
            sentiment_pred = "Neutro"
        elif predicted_class > 0.5 and predicted_class < 1.0:
            sentiment_pred = "Negativo"
        else:
            sentiment_pred = "Muito negativo"
        
        return {'sentiment_num': predicted_class, 'sentiment_pred': sentiment_pred}


    def use_nlp_model(self, input_text):
        inputs = self.tokenizer(input_text, return_tensors='pt', truncation=True, padding=True).to(self.device)

        self.model.to(self.device)
        
        with torch.no_grad():
            outputs = self.model(**inputs)

        logits = outputs.logits
        predicted_class = torch.argmax(logits, dim=1).item()

        return predicted_class

