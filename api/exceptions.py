from rest_framework.views import exception_handler
from rest_framework import permissions
from django.contrib.auth.models import AnonymousUser

def custom_exception_handler(exc, context):

    handlers = {
        'ValidationError' : _handle_generic_error,
        'Http404' : _handle_generic_error,
        'PermissionDenied' : _handle_permissions_error,
        'NotAuthenticated' : _handle_authentication_error,
        'IntegrityError' : _handle_integrity_error,
        'MethodNotAllowed': _handle_not_allowed_error,
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
    request = context['request']
    method = request.method.lower()
    view = context['view']
    if response: 
        
        response.data = {
            'status_code' : response.status_code,
            'error' : str(exc),
        }

        if view.__class__.__name__ == 'EmpruntViewSet':

            if method == 'post':
                response.data['detail'] = 'You have to be a member to book a book'
            
            elif method in ['put', 'patch']:
                response.data['detail'] = 'You can\'t edit an Emprunt unless you\'re an admin'
            
            elif method == 'delete' or method in permissions.SAFE_METHODS:
                response.data['detail'] = 'This Emprunt doesn\'t belong to you.'
    
        elif view.__class__.__name__ == 'AvisViewSet':

            if method == 'post':
                response.data['detail'] = 'You have to be a member to share your opinion'
            
            elif method in ['delete', 'put', 'patch']:
                response.data['detail'] = 'This Emprunt doesn\'t belong to you, you can\'t delete it'

    return response

def _handle_not_allowed_error(exc, context, response):
    return response