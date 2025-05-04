from django.urls import path
from .views import (
    LoginView,
    LogoutView,
    RegisterView,
    VerifyEmailView,
    VerifyCodeView,
    ForgotPassword,
    UserView,
    ResetPassword,
    logout_view,
    RefreshTokenView,
)
from django.shortcuts import redirect


from .views import (
    LoginView,
    LogoutView,
    RegisterView,
    UserView,
    RefreshTokenView,
    logout_view,
    UserGenresView,
    CountryView,
    # PhoneNumberView,
)
from .models import User
from .views import get_csrf_token
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.http import JsonResponse
import json
from rest_framework_simplejwt.tokens import AccessToken

# #@csrf_exempt
# def google_login_redirect(request):
#     return redirect("http://127.0.0.1:8000/accounts/google/login/?process=login")


@csrf_protect
def google_login_redirect(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))  # Parse JSON data
            email = data.get("email")
            first_name = data.get("given_name")
            last_name = data.get("family_name")
            google_id = data.get("sub")  # Google unique ID
            email_verified = data.get("email_verified", False)

            if not email or not google_id:
                return JsonResponse({"error": "Missing required fields"}, status=400)

            # Check if user exists, create if not
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "first_name": first_name,
                    "last_name": last_name,
                    "google_id": google_id,  # Save Google ID
                    "email_verified": email_verified,
                },
            )

            # Update user details if they exist but missing values
            updated = False
            if not user.first_name and first_name:
                user.first_name = first_name
                updated = True
            if not user.last_name and last_name:
                user.last_name = last_name
                updated = True
            if not user.email_verified and email_verified:
                user.email_verified = email_verified
                updated = True
            if updated:
                user.save()

            # Generate JWT Token for the user
            access_token = str(AccessToken.for_user(user))

            return JsonResponse(
                {
                    "message": "Google login successful",
                    "user_created": created,
                    "user_id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "access_token": access_token,  # Sending token to frontend for authentication
                }
            )

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)


urlpatterns = [
    path("register", RegisterView.as_view(), name="register"),
    path("login", LoginView.as_view(), name="login"),
    path("user", UserView.as_view(), name="user"),
    path("refresh", RefreshTokenView.as_view(), name="refresh"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("google/", google_login_redirect, name="google-login"),
    path("logoutgoogle", logout_view),
    path("verifyEmailView", VerifyEmailView.as_view(), name="verifyEmailView"),
    path("verifyCode", VerifyCodeView.as_view(), name="verifyCode"),
    path("forgotPassword", ForgotPassword.as_view(), name="forgotPassword"),
    path("resetpassword", ResetPassword.as_view(), name="resetpassword"),
    path("user/genres", UserGenresView.as_view(), name="user-genres"),
    path("get-csrf-token/", get_csrf_token, name="get-csrf-token"),
    path("country/", CountryView.as_view(), name="set-country")
]
