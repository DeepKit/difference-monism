import pytest
from paginator import Paginator, PaginationError, PaginationResult


class TestPaginator:
    """分页器测试类"""
    
    @pytest.fixture
    def sample_data(self):
        """测试数据"""
        return [
            {'id': i, 'name': f'Item {i}', 'value': i * 10}
            for i in range(1, 51)  # 50条数据
        ]
    
    def test_basic_pagination(self, sample_data):
        """测试基本分页功能"""
        paginator = Paginator(sample_data)
        result = paginator.paginate(page=1, page_size=10)
        
        assert isinstance(result, PaginationResult)
        assert result.total == 50
        assert result.total_pages == 5
        assert result.current_page == 1
        assert result.page_size == 10
        assert len(result.data) == 10
        assert result.has_next is True
        assert result.has_prev is False
    
    def test_default_parameters(self, sample_data):
        """测试默认参数"""
        paginator = Paginator(sample_data)
        result = paginator.paginate()
        
        assert result.current_page == 1
        assert result.page_size == 10
        assert len(result.data) == 10
    
    def test_last_page(self, sample_data):
        """测试最后一页"""
        paginator = Paginator(sample_data)
        result = paginator.paginate(page=5, page_size=10)
        
        assert result.current_page == 5
        assert len(result.data) == 10
        assert result.has_next is False
        assert result.has_prev is True
    
    def test_partial_last_page(self):
        """测试不完整的最后一页"""
        data = [{'id': i} for i in range(1, 26)]  # 25条数据
        paginator = Paginator(data)
        result = paginator.paginate(page=3, page_size=10)
        
        assert result.total_pages == 3
        assert len(result.data) == 5  # 最后一页只有5条
        assert result.has_next is False
    
    def test_invalid_page_number(self, sample_data):
        """测试无效页码"""
        paginator = Paginator(sample_data)
        
        with pytest.raises(PaginationError, match="页码必须大于等于1"):
            paginator.paginate(page=0)
        
        with pytest.raises(PaginationError, match="页码必须大于等于1"):
            paginator.paginate(page=-1)
    
    def test_invalid_page_size(self, sample_data):
        """测试无效每页数量"""
        paginator = Paginator(sample_data)
        
        with pytest.raises(PaginationError, match="每页数量必须大于等于1"):
            paginator.paginate(page_size=0)
        
        with pytest.raises(PaginationError, match="每页数量不能超过100"):
            paginator.paginate(page_size=101)
    
    def test_invalid_parameter_types(self, sample_data):
        """测试无效参数类型"""
        paginator = Paginator(sample_data)
        
        with pytest.raises(PaginationError, match="页码必须是整数"):
            paginator.paginate(page="1")
        
        with pytest.raises(PaginationError, match="每页数量必须是整数"):
            paginator.paginate(page_size="10")
    
    def test_page_exceeds_total_pages(self, sample_data):
        """测试页码超出范围"""
        paginator = Paginator(sample_data)
        
        with pytest.raises(PaginationError, match="页码超出范围"):
            paginator.paginate(page=10, page_size=10)
    
    def test_empty_data(self):
        """测试空数据"""
        paginator = Paginator([])
        result = paginator.paginate()
        
        assert result.total == 0
        assert result.total_pages == 1
        assert len(result.data) == 0
        assert result.has_next is False
        assert result.has_prev is False
    
    def test_sort_ascending(self, sample_data):
        """测试升序排序"""
        paginator = Paginator(sample_data)
        result = paginator.paginate(page=1, page_size=5, sort_by='value', sort_order='asc')
        
        assert result.data[0]['value'] == 10
        assert result.data[1]['value'] == 20
        assert result.data[4]['value'] == 50
    
    def test_sort_descending(self, sample_data):
        """测试降序排序"""
        paginator = Paginator(sample_data)
        result = paginator.paginate(page=1, page_size=5, sort_by='value', sort_order='desc')
        
        assert result.data[0]['value'] == 500
        assert result.data[1]['value'] == 490
        assert result.data[4]['value'] == 460
    
    def test_sort_by_name(self, sample_data):
        """测试按名称排序"""
        paginator = Paginator(sample_data)
        result = paginator.paginate(page=1, page_size=5, sort_by='name', sort_order='asc')
        
        assert result.data[0]['name'] == 'Item 1'
        assert result.data[1]['name'] == 'Item 10'
    
    def test_sort_invalid_field(self, sample_data):
        """测试无效排序字段"""
        paginator = Paginator(sample_data)
        
        with pytest.raises(PaginationError, match="排序字段.*不存在"):
            paginator.paginate(sort_by='invalid_field')
    
    def test_max_page_size_boundary(self, sample_data):
        """测试最大每页数量边界"""
        paginator = Paginator(sample_data)
        
        # 正好100应该可以
        result = paginator.paginate(page_size=100)
        assert result.page_size == 100
        
        # 101应该失败
        with pytest.raises(PaginationError):
            paginator.paginate(page_size=101)
    
    def test_pagination_consistency(self, sample_data):
        """测试分页一致性"""
        paginator = Paginator(sample_data)
        
        # 获取所有页的数据
        all_items = []
        for page in range(1, 6):
            result = paginator.paginate(page=page, page_size=10)
            all_items.extend(result.data)
        
        # 验证总数据量
        assert len(all_items) == 50
        
        # 验证数据完整性
        ids = [item['id'] for item in all_items]
        assert sorted(ids) == list(range(1, 51))
