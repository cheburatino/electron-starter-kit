from abc import ABC
from infra.tool.postgres_client.postgres_client import PostgresClient
from repository.postgres.repository import Repository
from state.mixin.state_mixin import StateMixin
from repository.postgres.repository_mixin import RepositoryMixin


class LogicElement(StateMixin, RepositoryMixin, ABC):
    _db_client: PostgresClient
    _repository: Repository

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)

        original_init = cls.__init__

        def enhanced_init(self, el_id: str, db_client: PostgresClient, repository: Repository, *args, **kwargs):
            self.el_id = el_id
            self.category = self.__class__.__module__
            self._db_client = db_client
            self._repository = repository

            original_init(self, *args, **kwargs)
            
            cls.kit.object_container_manager.add(self, el_id)

        cls.__init__ = enhanced_init
    
    @classmethod
    def _instantiate(cls, el_id: str, db_client: PostgresClient, repository: Repository):
        return cls(el_id, db_client, repository)
