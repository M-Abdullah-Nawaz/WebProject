from rest_framework import serializers

from .models import User, UserGenres


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "phone_number",
            "country",
            "email",
            "password",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class UserGenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGenres
        fields = ["genre"]

    def create(self, validated_data):
        user = self.context["request"].user
        genre = validated_data["genre"]

        # Check if the relationship already exists
        user_genre, created = UserGenres.objects.get_or_create(user=user, genre=genre)
        if not created:
            raise serializers.ValidationError(
                "This genre is already selected for the user."
            )
        return user_genre


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["country"]


# class PhoneNumberSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ["phone_number"]
