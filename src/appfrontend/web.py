import logging
from uuid import uuid4

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.requests import Request
from starlette.responses import JSONResponse

from appbackend.views import router
from libshared.context import context
from libshared.errors import TradebroGeneralError
from libshared.fastapi import get_basic_app_params, generate_exception_handler
from libshared.logging import set_request_id

logger = logging.getLogger(__name__)

app_params = get_basic_app_params(
    service_name='appfrontend',
    environment=context.env,
    service_description='Account services to forward headers to other services',
    service_version='0.1.0',
    allow_swagger=True,
)
app = FastAPI(**app_params)

errhandler_500 = generate_exception_handler(500, client_error_message="Sorry, something wrong on our side")


def payment_general_exception_handler(request: Request, exc: TradebroGeneralError):
    exc_response = TradebroGeneralError(code=exc.code, message=exc.message)
    message = jsonable_encoder(exc_response)
    logger.exception({'message': message}, exc_info=exc)
    return JSONResponse(status_code=exc.code, content=message)


app.add_exception_handler(TradebroGeneralError, payment_general_exception_handler)
app.add_exception_handler(Exception, errhandler_500)


app.include_router(router)
