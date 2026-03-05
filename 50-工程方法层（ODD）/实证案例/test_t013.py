import pytest
from datetime import datetime
from log_analyzer import LogAnalyzer, LogLevel, LogEntry


@pytest.fixture
def sample_logs():
    return """2024-01-01 10:00:00 - INFO - Application started
2024-01-01 10:05:00 - DEBUG - Loading configuration
2024-01-01 10:10:00 - WARNING - High memory usage detected
2024-01-01 10:15:00 - ERROR - Database connection failed
2024-01-01 10:20:00 - INFO - Retrying connection
2024-01-01 10:25:00 - ERROR - Connection timeout
2024-01-01 10:30:00 - INFO - Application shutdown"""


@pytest.fixture
def analyzer():
    return LogAnalyzer()


def test_parse_text(analyzer, sample_logs):
    analyzer.parse_text(sample_logs)
    assert len(analyzer.entries) == 7


def test_parse_valid_log_line(analyzer):
    analyzer.parse_text("2024-01-01 12:00:00 - INFO - Test message")
    assert len(analyzer.entries) == 1
    assert analyzer.entries[0].level == LogLevel.INFO
    assert analyzer.entries[0].message == "Test message"


def test_parse_invalid_log_line(analyzer):
    analyzer.parse_text("Invalid log line")
    assert len(analyzer.entries) == 0


def test_filter_by_level(analyzer, sample_logs):
    analyzer.parse_text(sample_logs)
    errors = analyzer.filter_by_level([LogLevel.ERROR])
    assert len(errors) == 2
    assert all(e.level == LogLevel.ERROR for e in errors)
    info_and_debug = analyzer.filter_by_level([LogLevel.INFO, LogLevel.DEBUG])
    assert len(info_and_debug) == 4


def test_filter_by_level_empty_list(analyzer, sample_logs):
    analyzer.parse_text(sample_logs)
    with pytest.raises(ValueError, match="级别列表不能为空"):
        analyzer.filter_by_level([])


def test_filter_by_time_range(analyzer, sample_logs):
    analyzer.parse_text(sample_logs)
    start = datetime(2024, 1, 1, 10, 10, 0)
    end = datetime(2024, 1, 1, 10, 20, 0)
    results = analyzer.filter_by_time_range(start, end)
    assert len(results) == 3
    results = analyzer.filter_by_time_range(start_time=start)
    assert len(results) == 5
    results = analyzer.filter_by_time_range(end_time=end)
    assert len(results) == 5


def test_search_keyword(analyzer, sample_logs):
    analyzer.parse_text(sample_logs)
    results = analyzer.search_keyword("connection")
    assert len(results) == 3
    results = analyzer.search_keyword("Connection", case_sensitive=True)
    assert len(results) == 1


def test_search_keyword_empty(analyzer, sample_logs):
    analyzer.parse_text(sample_logs)
    with pytest.raises(ValueError, match="关键词不能为空"):
        analyzer.search_keyword("")


def test_get_statistics(analyzer, sample_logs):
    analyzer.parse_text(sample_logs)
    stats = analyzer.get_statistics()
    assert stats["INFO"] == 3
    assert stats["DEBUG"] == 1
    assert stats["WARNING"] == 1
    assert stats["ERROR"] == 2


def test_get_statistics_empty(analyzer):
    stats = analyzer.get_statistics()
    assert all(count == 0 for count in stats.values())


def test_filter_combined(analyzer, sample_logs):
    analyzer.parse_text(sample_logs)
    results = analyzer.filter_combined(
        levels=[LogLevel.ERROR, LogLevel.WARNING],
        start_time=datetime(2024, 1, 1, 10, 10, 0),
        keyword="connection"
    )
    assert len(results) == 2
    assert all(e.level in [LogLevel.ERROR, LogLevel.WARNING] for e in results)


def test_clear(analyzer, sample_logs):
    analyzer.parse_text(sample_logs)
    assert len(analyzer.entries) > 0
    analyzer.clear()
    assert len(analyzer.entries) == 0


def test_parse_file_not_found(analyzer):
    with pytest.raises(ValueError, match="文件不存在"):
        analyzer.parse_file("nonexistent.log")


def test_multiple_parse_calls(analyzer):
    analyzer.parse_text("2024-01-01 12:00:00 - INFO - First")
    analyzer.parse_text("2024-01-01 12:01:00 - ERROR - Second")
    assert len(analyzer.entries) == 2
