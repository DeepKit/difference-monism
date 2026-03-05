import pytest
import json
import yaml
import os
from pathlib import Path
from config_manager import (
    ConfigManager,
    ConfigError,
    ConfigLoadError,
    ConfigValidationError
)


@pytest.fixture
def temp_json_config(tmp_path):
    config_file = tmp_path / "config.json"
    config_data = {
        "database": {"host": "localhost", "port": 5432},
        "debug": True,
        "timeout": 30
    }
    config_file.write_text(json.dumps(config_data))
    return config_file


@pytest.fixture
def temp_yaml_config(tmp_path):
    config_file = tmp_path / "config.yaml"
    config_data = {
        "database": {"host": "localhost", "port": 5432},
        "debug": True,
        "timeout": 30
    }
    config_file.write_text(yaml.dump(config_data))
    return config_file


@pytest.fixture
def cleanup_env():
    original_env = os.environ.copy()
    yield
    os.environ.clear()
    os.environ.update(original_env)


class TestConfigManager:
    def test_load_json_config(self, temp_json_config):
        manager = ConfigManager(config_path=str(temp_json_config))
        assert manager.get("debug") is True
        assert manager.get("timeout") == 30
        assert manager.get_nested("database.host") == "localhost"
        assert manager.get_nested("database.port") == 5432
    
    def test_load_yaml_config(self, temp_yaml_config):
        manager = ConfigManager(config_path=str(temp_yaml_config))
        assert manager.get("debug") is True
        assert manager.get("timeout") == 30
    
    def test_default_values(self):
        defaults = {"app_name": "MyApp", "version": "1.0.0", "debug": False}
        manager = ConfigManager(defaults=defaults)
        assert manager.get("app_name") == "MyApp"
        assert manager.get("version") == "1.0.0"
        assert manager.get("debug") is False
    
    def test_file_overrides_defaults(self, temp_json_config):
        defaults = {"debug": False, "timeout": 60}
        manager = ConfigManager(config_path=str(temp_json_config), defaults=defaults)
        assert manager.get("debug") is True
        assert manager.get("timeout") == 30
    
    def test_env_overrides_file(self, temp_json_config, cleanup_env):
        os.environ["APP_DEBUG"] = "false"
        os.environ["APP_TIMEOUT"] = "120"
        manager = ConfigManager(config_path=str(temp_json_config), env_prefix="APP_")
        assert manager.get("debug") is False
        assert manager.get("timeout") == 120
    
    def test_env_json_parsing(self, cleanup_env):
        os.environ["APP_CONFIG"] = '{"key": "value", "number": 42}'
        manager = ConfigManager(env_prefix="APP_")
        config_value = manager.get("config")
        assert isinstance(config_value, dict)
        assert config_value["key"] == "value"
    
    def test_validation_success(self, temp_json_config):
        def validator(config):
            assert "debug" in config
            assert config["timeout"] > 0
        manager = ConfigManager(config_path=str(temp_json_config), validator=validator)
        assert manager.get("debug") is True
    
    def test_validation_failure(self, temp_json_config):
        def validator(config):
            if config.get("timeout", 0) < 100:
                raise ValueError("timeout必须大于100")
        with pytest.raises(ConfigValidationError) as exc_info:
            ConfigManager(config_path=str(temp_json_config), validator=validator)
        assert "timeout必须大于100" in str(exc_info.value)
    
    def test_get_with_default(self):
        manager = ConfigManager()
        assert manager.get("nonexistent") is None
        assert manager.get("nonexistent", "default") == "default"
    
    def test_get_nested(self, temp_json_config):
        manager = ConfigManager(config_path=str(temp_json_config))
        assert manager.get_nested("database.host") == "localhost"
        assert manager.get_nested("database.port") == 5432
        assert manager.get_nested("database.nonexistent", "default") == "default"
    
    def test_set_config(self):
        manager = ConfigManager()
        manager.set("new_key", "new_value")
        assert manager.get("new_key") == "new_value"
    
    def test_dict_access(self, temp_json_config):
        manager = ConfigManager(config_path=str(temp_json_config))
        assert manager["debug"] is True
        assert manager["timeout"] == 30
        with pytest.raises(KeyError):
            _ = manager["nonexistent"]
    
    def test_contains(self, temp_json_config):
        manager = ConfigManager(config_path=str(temp_json_config))
        assert "debug" in manager
        assert "timeout" in manager
        assert "nonexistent" not in manager
    
    def test_to_dict(self, temp_json_config):
        manager = ConfigManager(config_path=str(temp_json_config))
        config_dict = manager.to_dict()
        assert isinstance(config_dict, dict)
        assert config_dict["debug"] is True
    
    def test_manual_reload(self, temp_json_config):
        manager = ConfigManager(config_path=str(temp_json_config))
        assert manager.get("timeout") == 30
        new_config = {"timeout": 60, "debug": False}
        temp_json_config.write_text(json.dumps(new_config))
        manager.reload()
        assert manager.get("timeout") == 60
    
    def test_invalid_file_format(self, tmp_path):
        config_file = tmp_path / "config.txt"
        config_file.write_text("invalid format")
        with pytest.raises(ConfigLoadError) as exc_info:
            ConfigManager(config_path=str(config_file))
        assert "不支持的配置文件格式" in str(exc_info.value)
    
    def test_nonexistent_file(self):
        manager = ConfigManager(config_path="nonexistent.json", defaults={"key": "value"})
        assert manager.get("key") == "value"
    
    def test_thread_safety(self, temp_json_config):
        from threading import Thread
        manager = ConfigManager(config_path=str(temp_json_config))
        results = []
        def read_config():
            for _ in range(100):
                results.append(manager.get("timeout"))
        threads = [Thread(target=read_config) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert all(r == 30 for r in results)
