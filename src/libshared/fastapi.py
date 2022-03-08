import traceback
from typing import Dict, Callable

from starlette.responses import JSONResponse

from libshared.logging import logger


def get_basic_app_params(
    *,
    service_name: str,
    environment: str,
    service_description: str = '',
    service_version: str = '0.1.0',
    docs_url: str = '/swagger',
    redoc_url: str = '/docs',
    allow_swagger: bool = False,
) -> Dict[str, str | None]:
    assert environment in {'prod', 'staging', 'dev'}, f'The environment {environment} is invalid'

    app_params = {
        'title': f'{service_name.capitalize()} API',
        'description': service_description,
        'version': service_version,
        'docs_url': docs_url,
        'redoc_url': redoc_url,
    }

    if not allow_swagger:
        app_params.update({'openapi_url': None, 'docs_url': None, 'redoc_url': None})

    return app_params


def generate_exception_handler(
    status_code: int,
    *,
    client_error_message: str | Callable[[Exception], str] = '',
):
    def handler(request, exception):
        content = {'error': client_error_message(exception) if callable(client_error_message) else client_error_message}
        logger.error(traceback.format_exception(type(exception), exception, exception.__traceback__))
        return JSONResponse(content=content, status_code=status_code)

    return handler
