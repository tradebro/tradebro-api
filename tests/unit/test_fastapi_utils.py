from starlette.responses import JSONResponse

from libshared.fastapi import get_basic_app_params, generate_exception_handler


def test_get_basic_app_params_defaults():
    """
    GIVEN get_basic_app_params called with default required params
    WHEN the method is called
    THEN optional params is defined with its default values
    """
    params = get_basic_app_params(service_name='testname', environment='dev')

    assert params.get('title') == 'Testname API'
    assert params.get('description') == ''
    assert params.get('version') == '0.1.0'
    assert params.get('docs_url') is None
    assert params.get('redoc_url') is None


def test_generate_exception_handler():
    """
    GIVEN generate_exception_handler called for an exception
    WHEN the method is called
    THEN the returned callable when called should return a JSONResponse object
    """
    exc_handler = generate_exception_handler(status_code=500, client_error_message='Sorry something went wrong')

    assert callable(exc_handler)

    response = exc_handler(request=None, exception=Exception())

    assert isinstance(response, JSONResponse)
