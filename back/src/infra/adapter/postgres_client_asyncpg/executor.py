from infra.adapter.abc.postgres_client.executor import Executor as AbstractExecutor


class Executor(AbstractExecutor):
    async def execute_raw_sql(
        self,
        conn,
        sql_query: str,
        params: list | tuple,
        fetch: bool
    ) -> list | str | None:
        if conn is None:
            raise ValueError("Соединение (conn) не может быть None для выполнения запроса.")

        if fetch:
            return await conn.fetch(sql_query, *params)
        else:
            return await conn.execute(sql_query, *params) 