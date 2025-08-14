from core.env_manager.env_manager import EnvManager, Utils as EnvManagerUtils


def load_env():
    env_manager: EnvManager = EnvManagerUtils.get("env_manager")
    if env_manager:
        env_manager.load_env()
        print(f"Env loaded successfully. Environment: {env_manager.environment.value}")
    else:
        print("Env manager not found")