from core.config_manager.config_manager import ConfigManager, Utils as ConfigManagerUtils


def create_config_manager():
    config_manager: ConfigManager = ConfigManagerUtils.factory(
        obj_id="config_manager",
        ttl_seconds=-1
    )
    return config_manager