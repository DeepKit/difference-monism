class UnitConverter:
    def __init__(self):
        # 转换因子（相对于基准单位）
        self.conversions = {
            'length': {
                'm': 1, 'km': 1000, 'cm': 0.01, 'mm': 0.001,
                'mile': 1609.34, 'yard': 0.9144, 'foot': 0.3048, 'inch': 0.0254
            },
            'weight': {
                'kg': 1, 'g': 0.001, 'mg': 0.000001, 't': 1000,
                'lb': 0.453592, 'oz': 0.0283495
            },
            'volume': {
                'l': 1, 'ml': 0.001, 'm3': 1000,
                'gallon': 3.78541, 'quart': 0.946353, 'cup': 0.236588
            },
            'temperature': {
                'c': lambda x: x, 'f': lambda x: (x - 32) * 5/9, 'k': lambda x: x - 273.15
            }
        }
        
        self.temp_to = {
            'c': lambda x: x, 'f': lambda x: x * 9/5 + 32, 'k': lambda x: x + 273.15
        }
    
    def convert(self, value, from_unit, to_unit, category):
        from_unit, to_unit = from_unit.lower(), to_unit.lower()
        
        if category == 'temperature':
            celsius = self.conversions['temperature'][from_unit](value)
            return self.temp_to[to_unit](celsius)
        
        if category not in self.conversions:
            raise ValueError(f"不支持的类别: {category}")
        
        units = self.conversions[category]
        if from_unit not in units or to_unit not in units:
            raise ValueError(f"不支持的单位: {from_unit} 或 {to_unit}")
        
        base_value = value * units[from_unit]
        return base_value / units[to_unit]


# 使用示例
converter = UnitConverter()
print(converter.convert(100, 'cm', 'm', 'length'))        # 1.0
print(converter.convert(1, 'kg', 'lb', 'weight'))         # 2.20462
print(converter.convert(32, 'f', 'c', 'temperature'))     # 0.0
print(converter.convert(1, 'l', 'ml', 'volume'))          # 1000.0