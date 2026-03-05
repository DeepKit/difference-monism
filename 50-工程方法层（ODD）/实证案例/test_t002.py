"""购物车系统测试"""
import pytest
from shopping_cart import (
    ShoppingCart, Product, 
    InsufficientStockError, ProductNotFoundError, InvalidQuantityError
)


@pytest.fixture
def cart():
    """创建购物车实例"""
    cart = ShoppingCart()
    
    # 注册测试商品
    cart.register_product(Product("P001", "苹果", 10.0, 100))
    cart.register_product(Product("P002", "香蕉", 5.0, 50))
    cart.register_product(Product("P003", "橙子", 8.0, 30))
    cart.register_product(Product("P004", "西瓜", 25.0, 10))
    
    return cart


class TestAddItem:
    """测试添加商品功能"""
    
    def test_add_single_item(self, cart):
        """测试添加单个商品"""
        cart.add_item("P001", 2)
        assert len(cart.items) == 1
        assert cart.items["P001"].quantity == 2
    
    def test_add_multiple_items(self, cart):
        """测试添加多个不同商品"""
        cart.add_item("P001", 2)
        cart.add_item("P002", 3)
        assert len(cart.items) == 2
        assert cart.items["P001"].quantity == 2
        assert cart.items["P002"].quantity == 3
    
    def test_add_same_item_twice(self, cart):
        """测试重复添加同一商品"""
        cart.add_item("P001", 2)
        cart.add_item("P001", 3)
        assert cart.items["P001"].quantity == 5
    
    def test_add_nonexistent_product(self, cart):
        """测试添加不存在的商品"""
        with pytest.raises(ProductNotFoundError) as exc_info:
            cart.add_item("P999", 1)
        assert "商品不存在" in str(exc_info.value)
    
    def test_add_invalid_quantity(self, cart):
        """测试添加无效数量"""
        with pytest.raises(InvalidQuantityError):
            cart.add_item("P001", 0)
        
        with pytest.raises(InvalidQuantityError):
            cart.add_item("P001", -1)
    
    def test_add_exceeds_stock(self, cart):
        """测试添加数量超过库存"""
        with pytest.raises(InsufficientStockError) as exc_info:
            cart.add_item("P001", 101)
        assert "库存不足" in str(exc_info.value)
    
    def test_add_multiple_times_exceeds_stock(self, cart):
        """测试多次添加累计超过库存"""
        cart.add_item("P004", 8)  # 西瓜库存10
        with pytest.raises(InsufficientStockError):
            cart.add_item("P004", 3)  # 8+3=11 > 10


class TestUpdateQuantity:
    """测试修改数量功能"""
    
    def test_update_quantity(self, cart):
        """测试修改商品数量"""
        cart.add_item("P001", 2)
        cart.update_quantity("P001", 5)
        assert cart.items["P001"].quantity == 5
    
    def test_update_to_zero_removes_item(self, cart):
        """测试修改数量为0会删除商品"""
        cart.add_item("P001", 2)
        cart.update_quantity("P001", 0)
        assert "P001" not in cart.items
    
    def test_update_nonexistent_item(self, cart):
        """测试修改不存在的商品"""
        with pytest.raises(ProductNotFoundError):
            cart.update_quantity("P001", 5)
    
    def test_update_exceeds_stock(self, cart):
        """测试修改数量超过库存"""
        cart.add_item("P001", 2)
        with pytest.raises(InsufficientStockError):
            cart.update_quantity("P001", 101)
    
    def test_update_negative_quantity(self, cart):
        """测试修改为负数"""
        cart.add_item("P001", 2)
        with pytest.raises(InvalidQuantityError):
            cart.update_quantity("P001", -1)


class TestRemoveItem:
    """测试删除商品功能"""
    
    def test_remove_item(self, cart):
        """测试删除商品"""
        cart.add_item("P001", 2)
        cart.add_item("P002", 3)
        cart.remove_item("P001")
        assert "P001" not in cart.items
        assert len(cart.items) == 1
    
    def test_remove_nonexistent_item(self, cart):
        """测试删除不存在的商品"""
        with pytest.raises(ProductNotFoundError):
            cart.remove_item("P001")


class TestPriceCalculation:
    """测试价格计算功能"""
    
    def test_subtotal_single_item(self, cart):
        """测试单个商品小计"""
        cart.add_item("P001", 2)  # 10 * 2 = 20
        assert cart.get_subtotal() == 20.0
    
    def test_subtotal_multiple_items(self, cart):
        """测试多个商品小计"""
        cart.add_item("P001", 2)  # 10 * 2 = 20
        cart.add_item("P002", 3)  # 5 * 3 = 15
        assert cart.get_subtotal() == 35.0
    
    def test_no_discount_under_100(self, cart):
        """测试不满100无折扣"""
        cart.add_item("P001", 5)  # 50元
        assert cart.calculate_discount(50) == 0
        assert cart.get_total() == 50.0
    
    def test_discount_100_to_199(self, cart):
        """测试满100减10"""
        cart.add_item("P001", 10)  # 100元
        assert cart.calculate_discount(100) == 10
        assert cart.get_total() == 90.0
        
        cart.clear()
        cart.add_item("P001", 15)  # 150元
        assert cart.get_total() == 140.0
    
    def test_discount_200_and_above(self, cart):
        """测试满200减30"""
        cart.add_item("P001", 20)  # 200元
        assert cart.calculate_discount(200) == 30
        assert cart.get_total() == 170.0
        
        cart.clear()
        cart.add_item("P004", 10)  # 250元
        assert cart.get_total() == 220.0
    
    def test_discount_edge_cases(self, cart):
        """测试折扣边界情况"""
        # 99.99元 - 无折扣
        cart.add_item("P001", 9)
        cart.add_item("P002", 1)  # 90 + 5 = 95
        assert cart.get_total() == 95.0
        
        cart.clear()
        # 199.99元 - 减10
        cart.add_item("P001", 19)
        cart.add_item("P002", 2)  # 190 + 10 = 200
        assert cart.get_total() == 170.0


class TestSummary:
    """测试购物车摘要功能"""
    
    def test_summary_structure(self, cart):
        """测试摘要数据结构"""
        cart.add_item("P001", 2)
        cart.add_item("P002", 3)
        
        summary = cart.get_summary()
        
        assert "items" in summary
        assert "subtotal" in summary
        assert "discount" in summary
        assert "total" in summary
        assert len(summary["items"]) == 2
    
    def test_summary_values(self, cart):
        """测试摘要数值正确性"""
        cart.add_item("P001", 10)  # 100元
        cart.add_item("P002", 4)   # 20元
        
        summary = cart.get_summary()
        
        assert summary["subtotal"] == 120.0
        assert summary["discount"] == 10.0
        assert summary["total"] == 110.0


class TestClear:
    """测试清空购物车功能"""
    
    def test_clear_cart(self, cart):
        """测试清空购物车"""
        cart.add_item("P001", 2)
        cart.add_item("P002", 3)
        cart.clear()
        assert len(cart.items) == 0
        assert cart.get_total() == 0.0


class TestComplexScenarios:
    """测试复杂场景"""
    
    def test_full_shopping_flow(self, cart):
        """测试完整购物流程"""
        # 添加商品
        cart.add_item("P001", 5)   # 50元
        cart.add_item("P002", 10)  # 50元
        cart.add_item("P003", 5)   # 40元
        # 总计140元，应减10元
        
        assert cart.get_subtotal() == 140.0
        assert cart.get_total() == 130.0
        
        # 修改数量
        cart.update_quantity("P001", 10)  # 增加到100元
        # 总计190元，应减10元
        assert cart.get_total() == 180.0
        
        # 再添加商品达到200
        cart.add_item("P002", 2)  # 再加10元
        # 总计200元，应减30元
        assert cart.get_total() == 170.0
        
        # 删除商品
        cart.remove_item("P003")
        # 总计160元，应减10元
        assert cart.get_total() == 150.0
    
    def test_stock_management(self, cart):
        """测试库存管理"""
        # 添加接近库存上限
        cart.add_item("P004", 9)  # 西瓜库存10
        
        # 尝试再添加会失败
        with pytest.raises(InsufficientStockError):
            cart.add_item("P004", 2)
        
        # 修改为库存上限
        cart.update_quantity("P004", 10)
        assert cart.items["P004"].quantity == 10
        
        # 尝试超过库存上限会失败
        with pytest.raises(InsufficientStockError):
            cart.update_quantity("P004", 11)
