class CurrencyConverter:
    def __init__(self):
        self.rates = {}
        self.base_currency = 'USD'
    
    def set_base_currency(self, currency):
        """设置基准货币"""
        self.base_currency = currency.upper()
    
    def add_rate(self, from_currency, to_currency, rate):
        """添加汇率"""
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()
        
        if from_currency not in self.rates:
            self.rates[from_currency] = {}
        self.rates[from_currency][to_currency] = rate
        
        # 添加反向汇率
        if to_currency not in self.rates:
            self.rates[to_currency] = {}
        self.rates[to_currency][from_currency] = 1 / rate
    
    def convert(self, amount, from_currency, to_currency):
        """转换货币"""
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()
        
        if from_currency == to_currency:
            return amount
        
        # 直接转换
        if from_currency in self.rates and to_currency in self.rates[from_currency]:
            return amount * self.rates[from_currency][to_currency]
        
        # 通过基准货币转换
        if from_currency in self.rates and self.base_currency in self.rates[from_currency]:
            if to_currency in self.rates and self.base_currency in self.rates[to_currency]:
                base_amount = amount * self.rates[from_currency][self.base_currency]
                return base_amount * self.rates[self.base_currency][to_currency]
        
        raise ValueError(f"无法转换 {from_currency} 到 {to_currency}")
    
    def get_rate(self, from_currency, to_currency):
        """获取汇率"""
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()
        
        if from_currency == to_currency:
            return 1.0
        
        if from_currency in self.rates and to_currency in self.rates[from_currency]:
            return self.rates[from_currency][to_currency]
        
        raise ValueError(f"未找到 {from_currency} 到 {to_currency} 的汇率")


# 使用示例
if __name__ == "__main__":
    converter = CurrencyConverter()
    
    # 添加汇率
    converter.add_rate('USD', 'CNY', 7.2)
    converter.add_rate('USD', 'EUR', 0.92)
    converter.add_rate('EUR', 'GBP', 0.86)
    
    # 转换货币
    print(f"100 USD = {converter.convert(100, 'USD', 'CNY'):.2f} CNY")
    print(f"100 EUR = {converter.convert(100, 'EUR', 'USD'):.2f} USD")
    print(f"100 CNY = {converter.convert(100, 'CNY', 'USD'):.2f} USD")
    
    # 获取汇率
    print(f"USD to CNY 汇率: {converter.get_rate('USD', 'CNY')}")