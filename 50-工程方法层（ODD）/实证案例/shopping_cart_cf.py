class ShoppingCart:
    """购物车类"""
    
    def __init__(self):
        self.items = {}
    
    def add_item(self, product_id, quantity, price, stock=None):
        if quantity <= 0:
            return {'success': False, 'message': '数量必须大于0'}
        
        if stock is not None and quantity > stock:
            return {'success': False, 'message': f'库存不足，当前库存：{stock}'}
        
        if product_id in self.items:
            new_quantity = self.items[product_id]['quantity'] + quantity
            if stock is not None and new_quantity > stock:
                return {'success': False, 'message': f'库存不足，当前库存：{stock}'}
            self.items[product_id]['quantity'] = new_quantity
        else:
            self.items[product_id] = {
                'quantity': quantity,
                'price': price,
                'stock': stock
            }
        
        return {'success': True, 'message': '添加成功'}
    
    def update_quantity(self, product_id, quantity):
        if product_id not in self.items:
            return {'success': False, 'message': '商品不存在'}
        
        if quantity <= 0:
            return {'success': False, 'message': '数量必须大于0'}
        
        stock = self.items[product_id].get('stock')
        if stock is not None and quantity > stock:
            return {'success': False, 'message': f'库存不足，当前库存：{stock}'}
        
        self.items[product_id]['quantity'] = quantity
        return {'success': True, 'message': '修改成功'}
    
    def remove_item(self, product_id):
        if product_id not in self.items:
            return {'success': False, 'message': '商品不存在'}
        
        del self.items[product_id]
        return {'success': True, 'message': '删除成功'}
    
    def get_subtotal(self):
        subtotal = 0
        for item in self.items.values():
            subtotal += item['quantity'] * item['price']
        return subtotal
    
    def calculate_discount(self, subtotal):
        if subtotal >= 200:
            return 30
        elif subtotal >= 100:
            return 10
        return 0
    
    def calculate_total(self):
        subtotal = self.get_subtotal()
        discount = self.calculate_discount(subtotal)
        total = subtotal - discount
        return {'subtotal': subtotal, 'discount': discount, 'total': total}
    
    def get_items(self):
        return self.items.copy()
