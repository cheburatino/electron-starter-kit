class RootObject(ABC):

    _object_container_manager: ObjectContainerManager

    def __init_subclass__(cls) -> None:
        def enhance_init(self, *args, **kwargs):
            pass
        
        cls.__init__ = enhance_init

class Client(RootObject):