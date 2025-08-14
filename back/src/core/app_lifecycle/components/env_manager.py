from core.env_manager.env_manager import EnvManager, Utils as EnvManagerUtils


def create_env_manager():
    env_manager: EnvManager = EnvManagerUtils.factory(
        obj_id="env_manager",
        ttl_seconds=-1
    )
    return env_manager