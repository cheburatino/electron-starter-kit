from infra.tool.postgres_client.query_executor import Query, query_factory
from infra.tool.postgres_client.postgres_client import PostgresClient
from .repository import Repository


class TableCrud(Repository):
    def __init__(self, client: PostgresClient, table_name: str):
        self.client = client
        self.table_name = table_name
    
    async def get_by_id(self, id: int, res_columns: list = None) -> dict | None:
        if not id or id <= 0:
            raise ValueError(f"Для получения записи из {self.table_name} необходим валидный id (положительное число)")
            
        select_clause = "*"
        if isinstance(res_columns, list) and res_columns:
            select_clause = ", ".join(res_columns)
            
        sql = f"SELECT {select_clause} FROM {self.table_name} WHERE id = $1"
        query: Query = query_factory(sql, [id], fetch=True)
        result = await self.client.query_executor.execute_query(query)
        return result[0] if result else None
    
    async def get_list(
            self,
            filters: list | None = None,
            include_deleted: bool = False,
            res_columns: list | str | None = None,
            orderby: dict | None = None,
            page_count: int | None = None,
            page_number: int | None = None
            ) -> list[dict] | int:
        filters = filters or []
        
        select_clause = "*"
        is_count_query = False
        
        if isinstance(res_columns, list) and res_columns:
            select_clause = ", ".join(res_columns)
        elif isinstance(res_columns, str):
            select_clause = f"COUNT({res_columns})"
            is_count_query = True
        
        where_clauses = []
        params = []
        param_idx = 1
        
        if not include_deleted:
            where_clauses.append(f"deleted_at IS NULL")
        
        filter_parts = []
        
        for filter_item in filters:
            if isinstance(filter_item, str) and filter_item.upper() in ["AND", "OR"]:
                if filter_parts:
                    filter_parts.append(filter_item.upper())
            elif isinstance(filter_item, dict):
                field = filter_item.get("field")
                value = filter_item.get("value")
                operator = filter_item.get("operator", "=")
                
                if field and value is not None:
                    valid_operators = ["=", ">", "<", ">=", "<=", "<>", "!=", "LIKE", "ILIKE", "IN", "NOT IN", "IS", "IS NOT"]
                    if operator not in valid_operators:
                        raise ValueError(f"Недопустимый оператор '{operator}'. Допустимые операторы: {', '.join(valid_operators)}")
                    
                    if operator in ["IN", "NOT IN"] and isinstance(value, list):
                        placeholders = []
                        for item in value:
                            placeholders.append(f"${param_idx}")
                            params.append(item)
                            param_idx += 1
                        filter_parts.append(f"{field} {operator} ({', '.join(placeholders)})")
                    elif operator in ["IS", "IS NOT"]:
                        if value is None:
                            filter_parts.append(f"{field} {operator} NULL")
                        else:
                            filter_parts.append(f"{field} {operator} ${param_idx}")
                            params.append(value)
                            param_idx += 1
                    else:
                        filter_parts.append(f"{field} {operator} ${param_idx}")
                        params.append(value)
                        param_idx += 1
        
        if filter_parts:
            final_filter = []
            for i, part in enumerate(filter_parts):
                if i > 0 and part not in ["AND", "OR"] and filter_parts[i-1] not in ["AND", "OR"]:
                    final_filter.append("AND")
                final_filter.append(part)
            
            where_clauses.append(" ".join(final_filter))
        
        sql = f"SELECT {select_clause} FROM {self.table_name}"
        
        if where_clauses:
            where_clause = " AND ".join(where_clauses)
            sql += f" WHERE {where_clause}"
        
        if orderby is not None:
            order_fields = orderby.get("field", ["id"])
            if not isinstance(order_fields, list):
                order_fields = ["id"]
            
            order_direction = orderby.get("direction", "asc")
            if not isinstance(order_direction, str):
                order_direction = "asc"
            
            order_direction = order_direction.lower()
            if order_direction not in ["asc", "desc"]:
                order_direction = "asc"
            
            order_parts = [f"{field} {order_direction}" for field in order_fields]
            sql += f" ORDER BY {', '.join(order_parts)}"
        else:
            sql += " ORDER BY id ASC"
        
        if not is_count_query:
            if page_count is None:
                page_count = 10
            elif not isinstance(page_count, int) or page_count <= 0:
                raise ValueError("Параметр page_count должен быть положительным целым числом")

            if page_number is None:
                page_number = 1
            elif not isinstance(page_number, int) or page_number <= 0:
                raise ValueError("Параметр page_number должен быть положительным целым числом")
            
            offset = (page_number - 1) * page_count
            
            sql += f" LIMIT {page_count} OFFSET {offset}"
        
        query: Query = query_factory(sql, params, fetch=True)
        result = await self.client.query_executor.execute_query(query)
        
        if is_count_query and result:
            return result[0]['count']
        
        return result
        
    async def get_count(self, filters: list = None, include_deleted: bool = False, field_name: str = '*') -> int:
        return await self.list(filters, include_deleted, field_name)
    
    async def create(self, data: dict, res_columns: list = None) -> dict | None:
        returning_clause = "*"
        if isinstance(res_columns, list) and res_columns:
            returning_clause = ", ".join(res_columns)
        
        if not data:
            sql = f"INSERT INTO {self.table_name} DEFAULT VALUES RETURNING {returning_clause}"
            query: Query = query_factory(sql, [], fetch=True)
        else:
            columns = ", ".join(data.keys())
            placeholders = ", ".join([f"${i+1}" for i in range(len(data))])
            values = list(data.values())
            sql = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders}) RETURNING {returning_clause}"
            query: Query = query_factory(sql, values, fetch=True)
        
        result = await self.client.query_executor.execute_query(query)
        return result[0] if result else None
    
    async def update(self, id: int, data: dict, res_columns: list = None) -> dict | None:
        if not id or id <= 0:
            raise ValueError(f"Для обновления записи в {self.table_name} необходим валидный id (положительное число)")
            
        if not data:
            raise ValueError(f"Для обновления записи в {self.table_name} необходимо передать непустой словарь данных")
        
        set_clauses = []
        params = []
        param_idx = 1
        
        for key, value in data.items():
            set_clauses.append(f"{key} = ${param_idx}")
            params.append(value)
            param_idx += 1
        
        params.append(id)
        set_clause = ", ".join(set_clauses)
        
        returning_clause = "*"
        if isinstance(res_columns, list) and res_columns:
            returning_clause = ", ".join(res_columns)
        
        sql = f"UPDATE {self.table_name} SET {set_clause} WHERE id = ${param_idx} RETURNING {returning_clause}"
        query: Query = query_factory(sql, params, fetch=True)
        result = await self.client.query_executor.execute_query(query)
        
        return result[0] if result else None
    
    async def hard_delete(self, id: int, res_columns: list = None) -> dict | None:
        if not id or id <= 0:
            raise ValueError(f"Для удаления записи из {self.table_name} необходим валидный id (положительное число)")
            
        returning_clause = "*"
        if isinstance(res_columns, list) and res_columns:
            returning_clause = ", ".join(res_columns)
            
        sql = f"DELETE FROM {self.table_name} WHERE id = $1 RETURNING {returning_clause}"
        query: Query = query_factory(sql, [id], fetch=True)
        result = await self.client.query_executor.execute_query(query)
        return result[0] if result else None

    async def get_id_by_code(self, code: str) -> int | None:
        sql = f"SELECT id FROM {self.table_name} WHERE deleted_at IS NULL AND lower(code) = lower($1) LIMIT 1"
        query: Query = query_factory(sql, [code], fetch=True)
        result = await self.client.query_executor.execute_query(query)
        return result[0]["id"] if result else None

    async def soft_delete(self, id: int) -> dict | None:
        if not id or id <= 0:
            raise ValueError(f"Для удаления записи из {self.table_name} необходим валидный id (положительное число)")
        sql = f"UPDATE {self.table_name} SET deleted_at = now() WHERE id = $1 RETURNING *"
        query: Query = query_factory(sql, [id], fetch=True)
        result = await self.client.query_executor.execute_query(query)
        return result[0] if result else None
    