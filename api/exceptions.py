from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):

    handlers = {
        'ValidationError' : _handle_generic_error,
        'Http404' : _handle_generic_error,
        'PermissionDenied' : _handle_permissions_error,
        'NotAuthenticated' : _handle_authentication_error,
        'IntegrityError' : _handle_integrity_error,
    }

    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    
    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code

    exception_class = exc.__class__.__name__
    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)

    return response

def _handle_authentication_error(exc, context, response):
    if response : 
        response.data = {
            'detail' : 'Please login to proceed',
            'status_code' : response.status_code,
            'error' : str(exc)
        }

    return response

def _handle_generic_error(exc, context, response):
    return response

def _handle_integrity_error(exc, context, response):
    if response : 
        response.data = {
            'detail' : 'The data you are trying to insert don\'t fit our database requirements',
            'status_code' : response.status_code,
            'error' : str(exc),
        }

    return response

def _handle_permissions_error(exc, context, response):
    if response: 
        response.data = {
            'status_code' : response.status_code,
            'error' : str(exc),
        }

        if context:
            details = {
                'method': context.get('request').method,
                'path' : context.get('request').path,
                'permissions': [permission.__class__.__name__ for permission in context.get('view').get_permissions()]
            }
            response.data['details'] = details

    return response
