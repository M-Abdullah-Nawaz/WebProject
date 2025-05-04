# from rest_framework.views import exception_handler
# from rest_framework import status
# from rest_framework.exceptions import AuthenticationFailed

# def custom_exception_handler(exc, context):
#     response = exception_handler(exc, context)

#     if isinstance(exc, AuthenticationFailed):
#         response.status_code = status.HTTP_401_UNAUTHORIZED

#     return response


from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """
    Custom exception handler to return 401 for unauthenticated users
    and retain 403 for authenticated users lacking permissions.
    """
    # Call the default exception handler first
    response = exception_handler(exc, context)

    if isinstance(exc, NotAuthenticated):
        # If the user is not authenticated, return 401 instead of 403
        return Response(
            {"detail": "Authentication credentials were not provided."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

        # Handle AuthenticationFailed exceptions explicitly
    if isinstance(exc, AuthenticationFailed):
        # Example: returning 401 with a specific message for login failures
        return Response(
            {"detail": str(exc)},  # Use the exception message (e.g., "User not found!")
            status=status.HTTP_401_UNAUTHORIZED,
        )

    return response
