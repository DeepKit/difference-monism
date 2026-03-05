import pytest
from comment_system import CommentSystem


class TestCommentSystem:
    def test_add_comment_success(self):
        system = CommentSystem()
        result = system.add_comment('user1', 'content1', '这是一条评论内容')
        assert result['success'] is True
        assert result['comment_id'] == 1
    
    def test_sensitive_word_filter(self):
        system = CommentSystem(sensitive_words=['敏感词', '违禁'])
        result = system.add_comment('user1', 'content1', '这包含敏感词内容')
        assert result['success'] is False
        assert '敏感词' in result['message']
    
    def test_comment_length_too_short(self):
        system = CommentSystem()
        result = system.add_comment('user1', 'content1', '短')
        assert result['success'] is False
        assert '过短' in result['message']
    
    def test_comment_length_too_long(self):
        system = CommentSystem()
        result = system.add_comment('user1', 'content1', 'a' * 501)
        assert result['success'] is False
        assert '过长' in result['message']
    
    def test_comment_length_valid(self):
        system = CommentSystem()
        result = system.add_comment('user1', 'content1', '12345')
        assert result['success'] is True
    
    def test_duplicate_comment(self):
        system = CommentSystem()
        system.add_comment('user1', 'content1', '第一次评论内容')
        result = system.add_comment('user1', 'content1', '第二次评论不同内容')
        assert result['success'] is False
        assert '重复' in result['message']
    
    def test_different_user_same_content(self):
        system = CommentSystem()
        system.add_comment('user1', 'content1', '用户1的评论')
        result = system.add_comment('user2', 'content1', '用户2的评论')
        assert result['success'] is True
    
    def test_reply_first_level(self):
        system = CommentSystem()
        r1 = system.add_comment('user1', 'content1', '这是父评论内容')
        parent_id = r1['comment_id']
        r2 = system.add_comment('user2', 'content1', '这是回复内容', parent_id=parent_id)
        assert r2['success'] is True
        comment = system.get_comment(r2['comment_id'])
        assert comment['parent_id'] == parent_id
    
    def test_reply_second_level_allowed(self):
        system = CommentSystem()
        r1 = system.add_comment('user1', 'content1', '一级评论内容')
        r2 = system.add_comment('user2', 'content1', '二级回复内容', parent_id=r1['comment_id'])
        # 二级回复允许 depth=1 -> depth=2
        assert r2['success'] is True
    
    def test_reply_third_level_forbidden(self):
        system = CommentSystem()
        r1 = system.add_comment('user1', 'content1', '第一层评论内容')
        r2 = system.add_comment('user2', 'content1', '第二层评论内容', parent_id=r1['comment_id'])
        r3 = system.add_comment('user3', 'content1', '第三层评论内容', parent_id=r2['comment_id'])
        # depth=2后再回复就是第3层，不允许
        assert r3['success'] is False
        assert '超过' in r3['message']
    
    def test_get_content_comments(self):
        system = CommentSystem()
        system.add_comment('user1', 'content1', '评论内容第一')
        system.add_comment('user2', 'content1', '评论内容第二')
        comments = system.get_content_comments('content1')
        assert len(comments) == 2
