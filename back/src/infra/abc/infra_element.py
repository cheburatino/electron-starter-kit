from state.mixin.state_mixin import StateMixin
from abc import ABC


class InfraElement(StateMixin, ABC):
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        original_init = cls.__init__

        def enhanced_init(self, el_id: str, *args, **kwargs):
            self.el_id = el_id
            self.category = self.__class__.__module__
            
            original_init(self, *args, **kwargs)
            
            self.__class__.kit.object_container_manager.add(self, el_id)

        cls.__init__ = enhanced_init
