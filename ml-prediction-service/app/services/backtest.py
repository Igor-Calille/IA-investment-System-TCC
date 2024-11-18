import numpy as np

class Backtest:
    def __init__(self):
        pass

    def check_signal_accuracy(self, data):
        # Calcular a mudança de preço do dia seguinte
        data['price_change'] = data['close'].shift(-1) - data['close']

        # Definir condições para um sinal correto de compra ou venda
        conditions = [
            (data['signal_ml'] > 0) & (data['price_change'] > 0),  # Compra seguida de aumento de preço
            (data['signal_ml'] < 0) & (data['price_change'] < 0),  # Venda seguida de queda de preço
        ]
        choices = [1, 1]  # Ambos são sinais corretos, independente de serem compra ou venda
        data['correct_signal'] = np.select(conditions, choices, default=0)

        # Calcular a acurácia do sinal
        correct_signals = data['correct_signal'].sum()
        total_signals = np.count_nonzero(data['signal_ml'])  # Conta todos os sinais emitidos, ignorando zeros

        # Debug print statements for signal and accuracy calculation
        accuracy = correct_signals / total_signals if total_signals > 0 else 0  # Evita divisão por zero

        return accuracy, total_signals, correct_signals
    
