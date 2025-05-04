from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.timezone import now

# from subscriptions.models import SubscriptionType

# SubscriptionTypeChoices=SubscriptionType.SubscriptionTypeChoices

# from subscriptions.models import Invoice
from django.apps import apps

# from utils.choices import Roles

from content.models import Genre


# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", User.Roles.ADMIN)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get("role") != User.Roles.ADMIN:  # Ensure the role is admin
            raise ValueError("Superuser must have role='admin'.")

        return self.create_user(email, password, **extra_fields)


# Custom User Model
class User(AbstractUser):
    # id = models.BigAutoField(primary_key=True) #By default it automatically creates id but I have mentioned it here anyways
    class Roles(models.TextChoices):
        ADMIN = "admin", "Admin"
        USER = "user", "User"
        SUPERUSER = "superuser", "Superuser"

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    email = models.EmailField(max_length=255, unique=True)
    # password = models.CharField(max_length=255)

    country = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.USER)
    preferred_language_id = models.PositiveIntegerField(blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=255, blank=True, null=True)
    email_verification_token_expires_at = models.DateTimeField(blank=True, null=True)
    password_reset_token = models.CharField(max_length=255, blank=True, null=True)
    password_reset_token_expires_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    google_id = models.CharField(max_length=512, blank=True, null=True)

    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    # Override save method
    def save(self, *args, **kwargs):
        if self.role not in dict(self.Roles.choices).keys():
            raise ValueError(
                f"Invalid role: {self.role}. Must be one of {', '.join(dict(self.Roles.choices).keys())}."
            )
        super().save(*args, **kwargs)


class UserGenres(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="genres")
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, related_name="user_genres"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "genre"], name="unique_user_genre")
        ]

    def __str__(self):
        return f"{self.user.id} - Genre {self.genre.id}"


# class UserSubscription(models.Model):

#     class StatusChoices(models.TextChoices):
#         ACTIVE = "active", "Active"
#         EXPIRED = "expired", "Expired"
#         CANCELLED = "cancelled", "Cancelled"

#     #subscription_type_id = models.ForeignKey(Invoice,on_delete=models.CASCADE, related_name='subscription_choice')

#     # subscription_type_id = models.CharField(max_length=10,choices=SubscriptionTypeChoices.choices, default=SubscriptionTypeChoices.FREE)

#     #subscription_type_id = models.ForeignKey(SubscriptionType,on_delete=models.CASCADE, related_name='subscription_choice')

#     # user = models.ForeignKey(
#     #     user_auth.User, on_delete=models.CASCADE, related_name="subscription"
#     # )

#     user = models.ForeignKey(
#         'user_auth.User', on_delete=models.CASCADE, related_name="subscription"
#     )

#     subscription_type_id = models.CharField(
#         max_length=10,
#         choices=apps.get_model('subscriptions', 'SubscriptionType').SubscriptionTypeChoices.choices,
#         default='free'
#     )

#     # subscription_type_id = models.CharField(
#     #     max_length=10,
#     #     choices=SubscriptionTypeChoices.choices,
#     #     default=SubscriptionTypeChoices.FREE,
#     # )

#     start_date = models.DateField(default=now)
#     end_date = models.DateField(null=True, blank=True)
#     status = models.CharField(max_length=10, choices=StatusChoices.choices)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.user.email} - {self.status}"


class UserSubscription(models.Model):

    # class SubscriptionTypeChoices(models.TextChoices):
    #     FREE = "free", "Free"
    #     BASIC = "basic", "Basic"
    #     STANDARD = "standard", "Standard"

    class StatusChoices(models.TextChoices):
        ACTIVE = "active", "Active"
        EXPIRED = "expired", "Expired"
        CANCELLED = "cancelled", "Cancelled"

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="subscription"
    )

    # We have to add dynamic reference because otherwise it was creating circular dependency
    # Other way around could be to move "UserSubscription" model to subscriptions app
    subscription_type = models.ForeignKey(
        "subscriptions.SubscriptionType",
        on_delete=models.CASCADE,
        related_name="user_subscriptions",
        default=1,
    )

    start_date = models.DateField(default=now)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=StatusChoices.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.status}"

    @staticmethod
    def get_subscription_choices():
        SubscriptionType = apps.get_model("subscriptions", "SubscriptionType")
        return SubscriptionType.SubscriptionTypeChoices.choices

    def save(self, *args, **kwargs):
        if not self.subscription_type_id:
            # Set choices dynamically before saving if not already set
            self._meta.get_field("subscription_type_id").choices = (
                self.get_subscription_choices()
            )
        super().save(*args, **kwargs)


"""
# Fetch the user with the given email
user = User.objects.get(email='example@gmail.com')

# Use the 'genres' related_name to access all UserGenres associated with the user
user_genres = user.genres.all()

# Extract the names of the genres from the related Genre objects
genre_names = [user_genre.genre.name for user_genre in user_genres]

# Print the list of genre names
print(genre_names)

"""
