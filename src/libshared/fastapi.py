import traceback
from typing import Dict, Callable

from slugify import slugify
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
    staging_openapi_prefix: str = None,
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

    if environment == 'staging':
        prefix = staging_openapi_prefix if staging_openapi_prefix else slugify(service_name)
        app_params.update({'openapi_prefix': f'/_svc/{prefix}'})
        logger.info(f'Staging OpenAPI Prefix is: {app_params.get("openapi_prefix")}')

    if not allow_swagger:
        app_params.update({'openapi_url': None, 'docs_url': None, 'redoc_url': None})

    return app_params


def generate_exception_handler(
    status_code: int,
    *,
    client_error_message: str | Callable[[Exception], str] = '',
    include_traceback: bool = False
):
    def handler(request, exception):
        content = {'error': client_error_message(exception) if callable(client_error_message) else client_error_message}
        if include_traceback:
            content['traceback'] = traceback.format_exception(type(exception), exception, exception.__traceback__)
        return JSONResponse(content=content, status_code=status_code)

    return handler


def request_validation_error_formatter(exc) -> str:
    return '\n'.join(f'{error["loc"][-1]}: {error["msg"]}' for error in exc.errors())


def integrity_error_formatter(error) -> str:
    error_code = error.orig.args[0]
    if error_code == 1062:
        return "Already exists"
    else:
        return f"{error.orig.args[1]} ({error_code})"


def assertion_formatter(exc) -> str:
    return exc.args[0] if exc.args else 'error'
