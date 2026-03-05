class CurrencyConverter:
    def __init__(self):
        self.rates = {
            'USD': 1.0,
            'EUR': 0.85,
            'GBP': 0.73,
            'JPY': 110.0,
            'CNY': 6.45
        }
    
    def convert(self, amount, from_currency, to_currency):
        if from_currency not in self.rates or to_currency not in self.rates:
            raise ValueError(f"不支持的货币: {from_currency} 或 {to_currency}")
        
        # 先转换为USD，再转换为目标货币
        amount_in_usd = amount / self.rates[from_currency]
        return amount_in_usd * self.rates[to_currency]
    
    def add_rate(self, currency, rate):
        self.rates[currency] = rate
    
    def get_rate(self, currency):
        return self.rates.get(currency)


# 使用示例
converter = CurrencyConverter()
result = converter.convert(100, 'USD', 'CNY')
print(f"100 USD = {result:.2f} CNY")