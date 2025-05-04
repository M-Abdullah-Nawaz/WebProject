from drf_yasg import openapi
import datetime
import jwt
import random
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.conf import settings
from core.settings import SECRET_KEY
from .models import User
from .serializers import UserSerializer
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.permissions import IsAuthenticated  # Import IsAuthenticated




from django.conf import settings
from core.settings import ACCESS_SECRET_KEY, REFRESH_SECRET_KEY
from .models import User, UserGenres
from .serializers import (
    UserSerializer,
    UserGenresSerializer,
    CountrySerializer,
    # PhoneNumberSerializer,
)
from .authentication.backends import JWTAuthentication
from content.models import Genre
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie


class RegisterView(APIView):

    authentication_classes = []
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=UserSerializer)
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(APIView):

    authentication_classes = []
    permission_classes = [AllowAny]


    @swagger_auto_schema(request_body=UserSerializer)
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed("User not found!")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password!")

        access_token = JWTAuthentication.generate_access_token(user)
        refresh_token = JWTAuthentication.generate_refresh_token(user)

        response = Response()
        response.set_cookie(
            key="jwt",
            value=access_token,
            httponly=True,
            secure=False,  # Use False in development for HTTP
            samesite="Strict",
            max_age=settings.ACCESS_TOKEN_LIFETIME * 60,
        )

        response.set_cookie(
            key="rft",
            value=refresh_token,
            httponly=True,
            secure=False,  # Use False in development for HTTP
            samesite="Strict",
            max_age=settings.REFRESH_TOKEN_LIFETIME * 24 * 60 * 60,
        )

        response.data = {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
        return response


class UserView(APIView):
    
    # @swagger_auto_schema(
    #     manual_parameters=[
    #         openapi.Parameter(
    #             'jwt',
    #             openapi.IN_COOKIE,
    #             description="JWT token for authentication",
    #             type=openapi.TYPE_STRING
    #         )
    #     ]
    # )

    def get(self, request):
        token = request.COOKIES.get("jwt")

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            # Specify the algorithms argument here
            payload = jwt.decode(token, ACCESS_SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        user = User.objects.filter(id=payload["id"]).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class RefreshTokenView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get("rft")

        if not refresh_token:
            raise AuthenticationFailed("Refresh token is missing.")

        try:
            payload = jwt.decode(
                refresh_token, REFRESH_SECRET_KEY, algorithms=["HS256"]
            )
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Refresh token has expired.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid refresh token.")

        user = User.objects.filter(id=payload["id"]).first()

        if user is None:
            raise AuthenticationFailed("User not found.")

        access_token = JWTAuthentication.generate_access_token(user)
        return Response({"access_token": access_token})


class CountryView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=CountrySerializer)
    def put(self, request):
        user = request.user
        serializer = CountrySerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Country set successfully"}, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class PhoneNumberView(APIView):
#     permission_classes = [IsAuthenticated]

#     @swagger_auto_schema(request_body=PhoneNumberSerializer)
#     def put(self, request):
#         user = request.user
#         serializer = PhoneNumberSerializer(user, data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 {"message": "Phone Number set successfully"}, status=status.HTTP_200_OK
#             )

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserGenresView(APIView):
    permission_classes = [IsAuthenticated]

    # @swagger_auto_schema(request_body=UserGenresSerializer)
    # def post(self, request):
    #     serializer = UserGenresSerializer(
    #         data=request.data, context={"request": request}
    #     )
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        user = request.user
        user_genres = UserGenres.objects.filter(user=user).select_related("genre")
        genres = [{"id": ug.genre.id, "name": ug.genre.name} for ug in user_genres]
        return Response(genres, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=UserGenresSerializer(many=True))
    def put(self, request):
        user = request.user
        UserGenres.objects.filter(user=user).delete()

        # Ensure request.data is treated as a list
        if not isinstance(request.data, list):
            return Response(
                {"error": "Expected a list of genres"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = UserGenresSerializer(
            data=request.data, context={"request": request}, many=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie("rft")
        response.data = {"message": "success"}
        return response


def logout_view(request):
    logout(request)
    return redirect("/")


# Email verification api
class VerifyEmailView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")

        if not email:
            raise ValidationError({"error": "Email field is required."})

        # Check if the email exists in the database
        user = User.objects.filter(email=email).first()

        if not user:
            return Response({"error": "Email not found."}, status=404)

        # Generate a 4-digit random code
        verification_code = random.randint(1000, 9999)

        
        # Here, we're assuming a custom field `verification_code` in the User model
        
        user.email_verification_token = verification_code
        user.save()

        # Send the code via email
        try:
            send_mail(
                subject="Your Verification Code",
                message=f"Your verification code is: {verification_code}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
            )
        except Exception as e:
            return Response({"error": f"Failed to send email: {str(e)}"}, status=500)

        return Response({"message": "Verification code sent successfully."}, status=200)

# verify code
class VerifyCodeView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        verification_code = request.data.get("code")

        if not email:
            raise ValidationError({"error": "Email field is required."})
        if not verification_code:
            raise ValidationError({"error": "Verification code field is required."})

        # Check if the user exists
        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"error": "User not found."}, status=404)

        # Check if the code matches
        if str(user.email_verification_token) != str(verification_code):
            return Response({"error": "Invalid verification code."}, status=400)

        # Code matches, mark the email as verified or take other actions
        user.email_verified = True
        user.email_verification_token = None  # Clear the token after use
        user.save()

        return Response({"message": "Email verified successfully."}, status=200)
    

# isko reset password name rakhna hai 
# change password
class ForgotPassword(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        new_password = request.data.get("new_password")

        if not email:
            raise ValidationError({"error": "Email field is required."})
        if not new_password:
            raise ValidationError({"error": "New password field is required."})

        # Check if the user exists
        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"error": "User not found."}, status=404)

        # Set the new password
        user.set_password(new_password)
        user.save()

        return Response({"message": "Password updated successfully."}, status=200)



class ResetPassword(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can reset their password / Login

    def post(self, request):
        # Get data from request
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not old_password:
            raise ValidationError({"error": "Old password field is required."})
        if not new_password:
            raise ValidationError({"error": "New password field is required."})

        user = request.user  # Since the user is authenticated, you can access the logged-in user

        # Check if the old password is correct
        if not user.check_password(old_password):
            raise ValidationError({"error": "Old password is incorrect."})

        # Check if new password is different from old password (optional)
        if old_password == new_password:
            raise ValidationError({"error": "New password cannot be the same as the old password."})

        # Set the new password
        user.set_password(new_password)
        user.save()

        return Response({"message": "Password reset successfully."}, status=200)
      
@ensure_csrf_cookie
def get_csrf_token(request):
    csrf_token = request.COOKIES.get("csrftoken")  # Fetch token from cookies
    if not csrf_token:
        return JsonResponse({"error": "CSRF token missing"}, status=400)
    return JsonResponse({"csrfToken": csrf_token})  # Ensure correct response
