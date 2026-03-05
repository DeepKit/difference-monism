class UnitConverter:
    """单位转换类"""
    
    # 长度转换基准：米
    LENGTH_UNITS = {
        'meter': 1,
        'm': 1,
        'kilometer': 1000,
        'km': 1000,
        'centimeter': 0.01,
        'cm': 0.01,
        'millimeter': 0.001,
        'mm': 0.001,
        'mile': 1609.344,
        'yard': 0.9144,
        'foot': 0.3048,
        'ft': 0.3048,
        'inch': 0.0254,
        'in': 0.0254
    }
    
    # 重量转换基准：千克
    WEIGHT_UNITS = {
        'kilogram': 1,
        'kg': 1,
        'gram': 0.001,
        'g': 0.001,
        'milligram': 0.000001,
        'mg': 0.000001,
        'ton': 1000,
        't': 1000,
        'pound': 0.453592,
        'lb': 0.453592,
        'ounce': 0.0283495,
        'oz': 0.0283495
    }
    
    # 时间转换基准：秒
    TIME_UNITS = {
        'second': 1,
        's': 1,
        'minute': 60,
        'min': 60,
        'hour': 3600,
        'h': 3600,
        'day': 86400,
        'd': 86400,
        'week': 604800,
        'month': 2592000,  # 30天
        'year': 31536000   # 365天
    }
    
    # 面积转换基准：平方米
    AREA_UNITS = {
        'square_meter': 1,
        'm2': 1,
        'square_kilometer': 1000000,
        'km2': 1000000,
        'square_centimeter': 0.0001,
        'cm2': 0.0001,
        'hectare': 10000,
        'acre': 4046.86,
        'square_foot': 0.092903,
        'ft2': 0.092903
    }
    
    def __init__(self):
        self.unit_types = {
            'length': self.LENGTH_UNITS,
            'weight': self.WEIGHT_UNITS,
            'time': self.TIME_UNITS,
            'area': self.AREA_UNITS
        }
    
    def convert(self, value, from_unit, to_unit, unit_type='length'):
        """
        转换单位
        
        Args:
            value: 要转换的数值
            from_unit: 源单位
            to_unit: 目标单位
            unit_type: 单位类型 ('length', 'weight', 'time', 'area', 'temperature')
        
        Returns:
            转换后的数值
        """
        if unit_type == 'temperature':
            return self._convert_temperature(value, from_unit, to_unit)
        
        if unit_type not in self.unit_types:
            raise ValueError(f"不支持的单位类型: {unit_type}")
        
        units = self.unit_types[unit_type]
        
        if from_unit not in units:
            raise ValueError(f"不支持的源单位: {from_unit}")
        if to_unit not in units:
            raise ValueError(f"不支持的目标单位: {to_unit}")
        
        # 先转换为基准单位，再转换为目标单位
        base_value = value * units[from_unit]
        result = base_value / units[to_unit]
        
        return result
    
    def _convert_temperature(self, value, from_unit, to_unit):
        """温度转换"""
        # 先转换为摄氏度
        if from_unit in ['celsius', 'c']:
            celsius = value
        elif from_unit in ['fahrenheit', 'f']:
            celsius = (value - 32) * 5/9
        elif from_unit in ['kelvin', 'k']:
            celsius = value - 273.15
        else:
            raise ValueError(f"不支持的温度单位: {from_unit}")
        
        # 从摄氏度转换为目标单位
        if to_unit in ['celsius', 'c']:
            return celsius
        elif to_unit in ['fahrenheit', 'f']:
            return celsius * 9/5 + 32
        elif to_unit in ['kelvin', 'k']:
            return celsius + 273.15
        else:
            raise ValueError(f"不支持的温度单位: {to_unit}")
    
    def length(self, value, from_unit, to_unit):
        """长度转换快捷方法"""
        return self.convert(value, from_unit, to_unit, 'length')
    
    def weight(self, value, from_unit, to_unit):
        """重量转换快捷方法"""
        return self.convert(value, from_unit, to_unit, 'weight')
    
    def time(self, value, from_unit, to_unit):
        """时间转换快捷方法"""
        return self.convert(value, from_unit, to_unit, 'time')
    
    def temperature(self, value, from_unit, to_unit):
        """温度转换快捷方法"""
        return self.convert(value, from_unit, to_unit, 'temperature')
    
    def area(self, value, from_unit, to_unit):
        """面积转换快捷方法"""
        return self.convert(value, from_unit, to_unit, 'area')


# 使用示例
if __name__ == '__main__':
    converter = UnitConverter()
    
    # 长度转换
    print(f"1 km = {converter.length(1, 'km', 'm')} m")
    print(f"100 cm = {converter.length(100, 'cm', 'm')} m")
    print(f"1 mile = {converter.length(1, 'mile', 'km')} km")
    
    # 重量转换
    print(f"1 kg = {converter.weight(1, 'kg', 'g')} g")
    print(f"1 lb = {converter.weight(1, 'lb', 'kg')} kg")
    
    # 温度转换
    print(f"0°C = {converter.temperature(0, 'c', 'f')}°F")
    print(f"100°C = {converter.temperature(100, 'c', 'k')} K")
    
    # 时间转换
    print(f"1 hour = {converter.time(1, 'hour', 'minute')} minutes")
    print(f"1 day = {converter.time(1, 'day', 'hour')} hours")
    
    # 面积转换
    print(f"1 km² = {converter.area(1, 'km2', 'm2')} m²")