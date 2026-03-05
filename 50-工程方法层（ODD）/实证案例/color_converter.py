class ColorConverter:
    """颜色转换工具类，支持多种颜色格式互转"""
    
    @staticmethod
    def rgb_to_hex(r, g, b):
        """RGB转HEX"""
        return f"#{r:02x}{g:02x}{b:02x}".upper()
    
    @staticmethod
    def hex_to_rgb(hex_color):
        """HEX转RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    @staticmethod
    def rgb_to_hsl(r, g, b):
        """RGB转HSL"""
        r, g, b = r / 255.0, g / 255.0, b / 255.0
        max_c = max(r, g, b)
        min_c = min(r, g, b)
        l = (max_c + min_c) / 2
        
        if max_c == min_c:
            h = s = 0
        else:
            d = max_c - min_c
            s = d / (2 - max_c - min_c) if l > 0.5 else d / (max_c + min_c)
            
            if max_c == r:
                h = (g - b) / d + (6 if g < b else 0)
            elif max_c == g:
                h = (b - r) / d + 2
            else:
                h = (r - g) / d + 4
            h /= 6
        
        return round(h * 360), round(s * 100), round(l * 100)
    
    @staticmethod
    def hsl_to_rgb(h, s, l):
        """HSL转RGB"""
        h, s, l = h / 360.0, s / 100.0, l / 100.0
        
        if s == 0:
            r = g = b = l
        else:
            def hue_to_rgb(p, q, t):
                if t < 0: t += 1
                if t > 1: t -= 1
                if t < 1/6: return p + (q - p) * 6 * t
                if t < 1/2: return q
                if t < 2/3: return p + (q - p) * (2/3 - t) * 6
                return p
            
            q = l * (1 + s) if l < 0.5 else l + s - l * s
            p = 2 * l - q
            r = hue_to_rgb(p, q, h + 1/3)
            g = hue_to_rgb(p, q, h)
            b = hue_to_rgb(p, q, h - 1/3)
        
        return round(r * 255), round(g * 255), round(b * 255)
    
    @staticmethod
    def rgb_to_hsv(r, g, b):
        """RGB转HSV"""
        r, g, b = r / 255.0, g / 255.0, b / 255.0
        max_c = max(r, g, b)
        min_c = min(r, g, b)
        v = max_c
        d = max_c - min_c
        s = 0 if max_c == 0 else d / max_c
        
        if max_c == min_c:
            h = 0
        else:
            if max_c == r:
                h = (g - b) / d + (6 if g < b else 0)
            elif max_c == g:
                h = (b - r) / d + 2
            else:
                h = (r - g) / d + 4
            h /= 6
        
        return round(h * 360), round(s * 100), round(v * 100)
    
    @staticmethod
    def hsv_to_rgb(h, s, v):
        """HSV转RGB"""
        h, s, v = h / 360.0, s / 100.0, v / 100.0
        
        i = int(h * 6)
        f = h * 6 - i
        p = v * (1 - s)
        q = v * (1 - f * s)
        t = v * (1 - (1 - f) * s)
        
        i %= 6
        if i == 0: r, g, b = v, t, p
        elif i == 1: r, g, b = q, v, p
        elif i == 2: r, g, b = p, v, t
        elif i == 3: r, g, b = p, q, v
        elif i == 4: r, g, b = t, p, v
        else: r, g, b = v, p, q
        
        return round(r * 255), round(g * 255), round(b * 255)
    
    @staticmethod
    def rgb_to_cmyk(r, g, b):
        """RGB转CMYK"""
        if (r, g, b) == (0, 0, 0):
            return 0, 0, 0, 100
        
        r, g, b = r / 255.0, g / 255.0, b / 255.0
        k = 1 - max(r, g, b)
        c = (1 - r - k) / (1 - k)
        m = (1 - g - k) / (1 - k)
        y = (1 - b - k) / (1 - k)
        
        return round(c * 100), round(m * 100), round(y * 100), round(k * 100)
    
    @staticmethod
    def cmyk_to_rgb(c, m, y, k):
        """CMYK转RGB"""
        c, m, y, k = c / 100.0, m / 100.0, y / 100.0, k / 100.0
        r = 255 * (1 - c) * (1 - k)
        g = 255 * (1 - m) * (1 - k)
        b = 255 * (1 - y) * (1 - k)
        
        return round(r), round(g), round(b)


# 使用示例
if __name__ == "__main__":
    converter = ColorConverter()
    
    # RGB转HEX
    print(converter.rgb_to_hex(255, 100, 50))  # #FF6432
    
    # HEX转RGB
    print(converter.hex_to_rgb("#FF6432"))  # (255, 100, 50)
    
    # RGB转HSL
    print(converter.rgb_to_hsl(255, 100, 50))  # (15, 100, 60)
    
    # HSL转RGB
    print(converter.hsl_to_rgb(15, 100, 60))  # (255, 102, 51)
    
    # RGB转HSV
    print(converter.rgb_to_hsv(255, 100, 50))  # (15, 80, 100)
    
    # HSV转RGB
    print(converter.hsv_to_rgb(15, 80, 100))  # (255, 102, 51)
    
    # RGB转CMYK
    print(converter.rgb_to_cmyk(255, 100, 50))  # (0, 61, 80, 0)
    
    # CMYK转RGB
    print(converter.cmyk_to_rgb(0, 61, 80, 0))  # (255, 99, 51)