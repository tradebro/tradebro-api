import logging
from uuid import uuid4

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.requests import Request
from fastapi.routing import APIRoute
from starlette.responses import JSONResponse

from appbackend.views import router
from libshared.context import context
from libshared.errors import TradebroGeneralError
from libshared.fastapi import get_basic_app_params, generate_exception_handler
from libshared.logging import set_request_id
from libshared.models.baserequestresponse import ErrorResponse

logger = logging.getLogger(__name__)

app_params = get_basic_app_params(
    service_name='appbackend',
    environment=context.env,
    service_description='Account services to forward headers to other services',
    service_version='0.1.0',
    allow_swagger=True,
)
app = FastAPI(**app_params)

errhandler_500 = generate_exception_handler(500, client_error_message="Sorry, something wrong on our side")


def general_exception_handler(request: Request, exc: TradebroGeneralError):
    exc_response = TradebroGeneralError(code=exc.code, message=exc.message)
    message = ErrorResponse(detail=exc_response.message).dict()
    logger.exception({'message': message}, exc_info=exc)
    return JSONResponse(status_code=exc.code, content=message)


app.add_exception_handler(TradebroGeneralError, general_exception_handler)
app.add_exception_handler(Exception, errhandler_500)


@app.middleware('http')
def before_request(request: Request, call_next):
    if request.url.path != '/public/hc':
        request.state.user_code = request.headers.get('x-forwarded-user')
        request.state.host = request.headers.get('host')

    # Unique Request ID
    set_request_id(new_request_id=uuid4())

    return call_next(request)


@app.get("/public/hc", status_code=200, tags=['system'])
def health_check():
    return "OK"


def use_route_names_as_operation_ids(app: FastAPI):
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name


app.include_router(router)
use_route_names_as_operation_ids(app=app)
