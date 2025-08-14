from state.live.object_container.models import TtlSecondsStrategy
from .kit import Kit
from .object_container_manager import ObjectContainerManager, ObjectContainerManagerConfig


def get_default_kit(element_cls: type) -> Kit:
    module_path = element_cls.__module__
    
    if module_path.startswith("infra"):
        object_container_manager_config = ObjectContainerManagerConfig(
            is_updatable=False,
            is_gettable=True,
            ttl_seconds=TtlSecondsStrategy.FOREVER.value
        )
    elif module_path.startswith("logic"):
        object_container_manager_config = ObjectContainerManagerConfig(
            is_updatable=True,
            is_gettable=False,
            ttl_seconds=TtlSecondsStrategy.MEDIUM.value
        )
    elif module_path.startswith("auth"):
        object_container_manager_config = ObjectContainerManagerConfig(
            is_updatable=True,
            is_gettable=False,
            ttl_seconds=TtlSecondsStrategy.SHORT.value
        )
    elif module_path.startswith("shared"):
        object_container_manager_config = ObjectContainerManagerConfig(
            is_updatable=True,
            is_gettable=False,
            ttl_seconds=TtlSecondsStrategy.SHORT.value
    )
    else:
        raise ValueError(
            f"Cannot determine default kit for {element_cls.__name__}. "
            f"Module path '{module_path}' doesn't match known patterns (infra, logic, auth, shared). "
            f"Please provide explicit kit parameter."
        )
    
    return Kit(ObjectContainerManager(object_container_manager_config, element_cls))