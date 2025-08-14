import re

from state.mixin.state_mixin import StateMixin
from repository.postgres.repository_mixin import RepositoryMixin


class CatalogItem:
    def __init__(self, code: str, title: str | None = None, id_value: int | None = None):
        self.code = code
        self.title = title or code
        self.id: int | None = id_value


class CatalogElement(StateMixin, RepositoryMixin):
    code: str | None = None
    title: str | None = None
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        original_init = cls.__init__

        def enhanced_init(self, el_id: str, db_client, repository, *args, **kw):
            self.el_id = el_id
            self.category = self.__class__.__module__
            self._db_client = db_client
            self._repository = repository

            original_init(self, *args, **kw)
            cls.kit.object_container_manager.add(self, el_id)

        cls.__init__ = enhanced_init

    @classmethod
    async def get_id_by_code(cls, code: str, db_client=None, repository=None) -> int:
        result = await super().get_id_by_code(code, db_client, repository)
        if result is None:
            raise ValueError(f"Элемент каталога с code='{code}' не найден в {cls._db_table_name}")
        return result

    @staticmethod
    def validate_code(code: str):
        pattern = r"^[A-Z0-9_]{1,50}$"
        if not isinstance(code, str) or not re.fullmatch(pattern, code):
            raise ValueError("code должен состоять из A-Z, 0-9 и _; без пробелов и дефисов; длина 1..50; верхний регистр")

    @classmethod
    async def create(cls, data: dict, db_client=None, repository=None):
        title = data.get("title")
        if not isinstance(title, str) or not title.strip():
            raise ValueError("title обязателен и не может быть пустым")
        code = data.get("code")
        cls.validate_code(code)
        return await super().create(data, db_client, repository)

    async def update(self, **data):
        if "title" in data:
            title = data.get("title")
            if not isinstance(title, str) or not title.strip():
                raise ValueError("title обязателен и не может быть пустым")
        if "code" in data:
            self.validate_code(data.get("code"))
        return await super().update(**data)
