# contact/serializers.py

from rest_framework import serializers

class ContactUsSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20)
    subject = serializers.CharField(max_length=255)
    message = serializers.CharField()
