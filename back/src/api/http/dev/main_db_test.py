from fastapi import APIRouter, HTTPException
from infra.tool.postgres_client.postgres_client import PostgresClient
from infra.tool.postgres_client.query_executor import Query, query_factory

router = APIRouter(prefix="/dev/main-db", tags=["dev", "main-db"])


@router.get("/select-now")
async def select_now():
    """Тест подключения к main_db - выполняет SELECT NOW()"""
    try:
        main_db_client: PostgresClient = PostgresClient.get("main_db")
        if not main_db_client:
            raise HTTPException(status_code=503, detail="Main DB client не найден в ObjectContainer")
        
        query: Query = query_factory(
            query="SELECT NOW() as current_time",
            params=[],
            fetch=True
        )
        
        result = await main_db_client.query_executor.execute_query(query)
        
        if result and len(result) > 0:
            current_time = result[0]["current_time"]
            return {
                "status": "success",
                "message": "Main database connection is working",
                "current_time": current_time.isoformat() if hasattr(current_time, 'isoformat') else str(current_time),
                "query": "SELECT NOW()"
            }
        else:
            return {
                "status": "error", 
                "message": "Query executed but no result returned",
                "query": "SELECT NOW()"
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка выполнения запроса к БД: {str(e)}") 