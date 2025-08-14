import sys
from dataclasses import dataclass, field
from collections.abc import Callable

from infra.adapter.abc.postgres_client.adapter import PostgresClient


@dataclass
class Query:
    query: str
    params: list | tuple | Callable[[any], list | tuple]
    fetch: bool = True
    result: any = field(init=False, default=None)


def query_factory(query: str, params: list | tuple | Callable[[any], list | tuple], fetch: bool = True) -> Query:
    return Query(query=query, params=params, fetch=fetch)


class QueryExecutor:
    def __init__(self, client_adapter: PostgresClient):
        if client_adapter is None:
            raise ValueError("Адаптер клиента (client_adapter) не может быть None")
        self._client_adapter = client_adapter

    async def execute_query(self, query_obj: Query, previous_result=None):
        if not isinstance(query_obj, Query):
            raise TypeError("Ожидается объект Query")

        current_params = query_obj.params
        if callable(current_params):
            if previous_result is not None:
                try:
                    current_params = current_params(previous_result)
                except Exception as e:
                    raise ValueError(f"Ошибка при вызове callable params для '{query_obj.query[:50]}...': {e}") from e
            else:
                raise ValueError(f"Callable params передан для '{query_obj.query[:50]}...' без previous_result.")

        if not isinstance(current_params, (list, tuple)):
            raise TypeError(f"Параметры должны быть list/tuple, получено {type(current_params)} для '{query_obj.query[:50]}...'")

        try:
            # Используем переданное транзакционное соединение если оно есть
            if hasattr(self, '_conn') and self._conn is not None:
                result = await self._client_adapter.executor.execute_raw_sql(
                    conn=self._conn, 
                    sql_query=query_obj.query, 
                    params=current_params, 
                    fetch=query_obj.fetch
                )
            else:
                # Выполняем запрос без транзакции - PostgreSQL сам сделает auto-commit
                async with self._client_adapter.connector.pool.acquire() as conn:
                    result = await self._client_adapter.executor.execute_raw_sql(
                        conn=conn, 
                        sql_query=query_obj.query,
                        params=current_params,
                        fetch=query_obj.fetch
                    )
            
            query_obj.result = result
            return result
        except Exception as e:
            print(f"Ошибка при выполнении запроса через QueryExecutor: {e}", file=sys.stderr)
            raise

    async def execute_queries(self, queries: list[Query]) -> list:
        results = []
        previous_result = None
        for query_obj in queries:
            current_result = await self.execute_query(query_obj, previous_result)
            results.append(current_result)
            previous_result = current_result
        return results