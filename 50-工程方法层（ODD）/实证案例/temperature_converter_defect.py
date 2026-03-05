class TemperatureConverter:
    @staticmethod
    def celsius_to_fahrenheit(celsius):
        return celsius * 9/5 + 32
    
    @staticmethod
    def fahrenheit_to_celsius(fahrenheit):
        return (fahrenheit - 32) * 5/9
    
    @staticmethod
    def celsius_to_kelvin(celsius):
        return celsius + 273.15
    
    @staticmethod
    def kelvin_to_celsius(kelvin):
        return kelvin - 273.15
    
    @staticmethod
    def fahrenheit_to_kelvin(fahrenheit):
        return TemperatureConverter.celsius_to_kelvin(
            TemperatureConverter.fahrenheit_to_celsius(fahrenheit)
        )
    
    @staticmethod
    def kelvin_to_fahrenheit(kelvin):
        return TemperatureConverter.celsius_to_fahrenheit(
            TemperatureConverter.kelvin_to_celsius(kelvin)
        )


# 使用示例
if __name__ == "__main__":
    print(f"100°C = {TemperatureConverter.celsius_to_fahrenheit(100)}°F")
    print(f"32°F = {TemperatureConverter.fahrenheit_to_celsius(32)}°C")
    print(f"0°C = {TemperatureConverter.celsius_to_kelvin(0)}K")