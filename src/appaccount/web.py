import logging

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.requests import Request
from starlette.responses import JSONResponse

from appaccount.views import router
from libaccount.context import context
from libaccount.errors import TradebroGeneralError
from libshared.fastapi import (
    get_basic_app_params,
    generate_exception_handler,
    request_validation_error_formatter,
    integrity_error_formatter,
    assertion_formatter,
)

logger = logging.getLogger(__name__)

app_params = get_basic_app_params(
    service_name='appaccount',
    environment=context.env,
    service_description='Account services to forward headers to other services',
    service_version='0.1.0',
    allow_swagger=True,
)
app = FastAPI(**app_params)

errhandler_400 = generate_exception_handler(400)
errhandler_400tb = generate_exception_handler(400, include_traceback=True)
errhandler_500 = generate_exception_handler(
    500, client_error_message="Sorry, something wrong on our side"
)
errhandler_req_validation = generate_exception_handler(
    400, client_error_message=request_validation_error_formatter
)
errhandler_integrity = generate_exception_handler(
    400, client_error_message=integrity_error_formatter
)
errhandler_assertion = generate_exception_handler(
    400, include_traceback=True, client_error_message=assertion_formatter
)
errhandler_http = generate_exception_handler(400, client_error_message=lambda exc: exc.detail)

app.add_exception_handler(RequestValidationError, errhandler_req_validation)
app.add_exception_handler(AssertionError, errhandler_assertion)
app.add_exception_handler(HTTPException, errhandler_http)
app.add_exception_handler(Exception, errhandler_500)


def payment_general_exception_handler(request: Request, exc: TradebroGeneralError):
    exc_response = TradebroGeneralError(code=exc.code, message=exc.message)
    message = jsonable_encoder(exc_response)
    logger.exception({'message': message}, exc_info=exc)
    return JSONResponse(status_code=exc.code, content=message)


app.add_exception_handler(TradebroGeneralError, payment_general_exception_handler)


@app.middleware('http')
def before_request(request: Request, call_next):
    if request.url.path != '/public/hc':
        request.state.user_code = request.headers.get('x-forwarded-user')
        request.state.host = request.headers.get('host')
    return call_next(request)


@app.get("/public/hc", status_code=200, tags=['system'])
def health_check():
    return "OK"


app.include_router(router)
