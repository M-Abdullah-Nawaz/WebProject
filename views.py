from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from django.core.mail import send_mail
from .serializers import ContactUsSerializer


class ContactUsView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=ContactUsSerializer)
    def post(self, request):
        serializer = ContactUsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        user_email = data["email"]
        full_name = f"{data['first_name']} {data['last_name']}"
        phone = data["phone"]
        subject = data["subject"]
        message = data["message"]

        email_message = (
            f"Name: {full_name}\n"
            f"Email: {user_email}\n"
            f"Phone: {phone}\n\n"
            f"Message:\n{message}"
        )

        try:
            send_mail(
                subject=f"[Contact Form] {subject}",
                message=email_message,
                from_email=user_email,
                recipient_list=["abdullahnawaz4120@gmail.com"],  
                fail_silently=False,
            )
        except Exception as e:
            return Response({"error": f"Failed to send message: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message": "Your message has been sent successfully!"}, status=status.HTTP_200_OK)
