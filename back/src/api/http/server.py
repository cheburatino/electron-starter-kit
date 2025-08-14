from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import logging


def setup_cors(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:8081"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def setup_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        errors = []
        for error in exc.errors():
            errors.append({
                'field': error['loc'][-1] if error['loc'] else None,
                'msg': error['msg'],
                'type': error['type']
            })
        logging.error(f"Ошибка валидации данных: {errors}")
        return JSONResponse(
            status_code=422,
            content={"detail": "Ошибка валидации данных", "errors": errors}
        )


def setup_server(app: FastAPI) -> None:
    setup_cors(app)
    setup_error_handlers(app) 