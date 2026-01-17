from rest_framework.views import exception_handler
from rest_framework.exceptions import (
    ValidationError,
    AuthenticationFailed,
    NotAuthenticated,
    PermissionDenied,
    NotFound,
)
from rest_framework import status
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    """
    This REPLACES all previously defined DRF exception responses
    """
    
    response = exception_handler(exc, context)
    print(exc)
    if response is None:
        return Response(
            {
                "success": False,
                "message": "Internal server error",
                "error": exc
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # 🔁 Replace ValidationError
    if isinstance(exc, ValidationError):
        response.data = {
            "success": False,
            "message": "Validation failed",
            "errors": response.data
        }

    # 🔁 Replace Auth errors (JWT / login)
    elif isinstance(exc, (AuthenticationFailed, NotAuthenticated)):
        response.data = {
            "success": False,
            "message": "Authentication failed"
        }

    # 🔁 Replace Permission errors
    elif isinstance(exc, PermissionDenied):
        response.data = {
            "success": False,
            "message": "Permission denied"
        }

    # 🔁 Replace Not Found
    elif isinstance(exc, NotFound):
        response.data = {
            "success": False,
            "message": "Resource not found"
        }
    

    # 🔁 Replace ALL remaining APIExceptions
    else:
        response.data = {
            "success": False,
            "message": str(exc)
        }

    return response

from rest_framework.exceptions import ValidationError as DRFValidationError

class ValidationError(DRFValidationError):
    default_detail = "Invalid request"
    default_code = "validation_error"