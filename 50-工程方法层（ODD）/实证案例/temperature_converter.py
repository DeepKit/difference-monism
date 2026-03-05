class TemperatureConverter:
    """温度转换类，支持摄氏度、华氏度和开尔文之间的转换"""
    
    @staticmethod
    def celsius_to_fahrenheit(celsius):
        """摄氏度转华氏度"""
        return (celsius * 9/5) + 32
    
    @staticmethod
    def celsius_to_kelvin(celsius):
        """摄氏度转开尔文"""
        return celsius + 273.15
    
    @staticmethod
    def fahrenheit_to_celsius(fahrenheit):
        """华氏度转摄氏度"""
        return (fahrenheit - 32) * 5/9
    
    @staticmethod
    def fahrenheit_to_kelvin(fahrenheit):
        """华氏度转开尔文"""
        celsius = TemperatureConverter.fahrenheit_to_celsius(fahrenheit)
        return TemperatureConverter.celsius_to_kelvin(celsius)
    
    @staticmethod
    def kelvin_to_celsius(kelvin):
        """开尔文转摄氏度"""
        return kelvin - 273.15
    
    @staticmethod
    def kelvin_to_fahrenheit(kelvin):
        """开尔文转华氏度"""
        celsius = TemperatureConverter.kelvin_to_celsius(kelvin)
        return TemperatureConverter.celsius_to_fahrenheit(celsius)
    
    @staticmethod
    def convert(value, from_unit, to_unit):
        """
        通用转换方法
        :param value: 温度值
        :param from_unit: 源单位 ('C', 'F', 'K')
        :param to_unit: 目标单位 ('C', 'F', 'K')
        :return: 转换后的温度值
        """
        from_unit = from_unit.upper()
        to_unit = to_unit.upper()
        
        if from_unit == to_unit:
            return value
        
        conversion_map = {
            ('C', 'F'): TemperatureConverter.celsius_to_fahrenheit,
            ('C', 'K'): TemperatureConverter.celsius_to_kelvin,
            ('F', 'C'): TemperatureConverter.fahrenheit_to_celsius,
            ('F', 'K'): TemperatureConverter.fahrenheit_to_kelvin,
            ('K', 'C'): TemperatureConverter.kelvin_to_celsius,
            ('K', 'F'): TemperatureConverter.kelvin_to_fahrenheit,
        }
        
        conversion_func = conversion_map.get((from_unit, to_unit))
        if conversion_func:
            return conversion_func(value)
        else:
            raise ValueError(f"不支持的转换: {from_unit} -> {to_unit}")


# 使用示例
if __name__ == "__main__":
    converter = TemperatureConverter()
    
    print(f"0°C = {converter.celsius_to_fahrenheit(0)}°F")
    print(f"100°C = {converter.celsius_to_kelvin(100)}K")
    print(f"32°F = {converter.fahrenheit_to_celsius(32)}°C")
    print(f"273.15K = {converter.kelvin_to_celsius(273.15)}°C")
    
    # 使用通用转换方法
    print(f"\n25°C = {converter.convert(25, 'C', 'F')}°F")
    print(f"77°F = {converter.convert(77, 'F', 'K')}K")