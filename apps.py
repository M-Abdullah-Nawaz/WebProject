from django.apps import AppConfig
from django.db.models.signals import post_migrate
import os


class UserAuthConfig(AppConfig):
    name = "user_auth"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        post_migrate.connect(setup_sites_and_social_apps, sender=self)


def setup_sites_and_social_apps(sender, **kwargs):
    """Ensure the required Site and SocialApp entries exist."""
    from django.contrib.sites.models import Site
    from allauth.socialaccount.models import SocialApp

    # Load credentials from environment variables
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    secret = os.getenv("GOOGLE_SECRET")

    # Ensure the Site exists
    site, _ = Site.objects.update_or_create(
        id=1,  # Overriding default "example.com"
        defaults={"domain": "127.0.0.1:8000", "name": "localhost"},
    )
    print(f"Site set to {site.domain} (ID: {site.id})")

    # Ensure the SocialApp exists for Google OAuth
    google_social_app, created = SocialApp.objects.update_or_create(
        provider="google",
        name="Google",
        defaults={
            "client_id": client_id,
            "secret": secret,
        },
    )

    # Ensure the SocialApp is associated with the correct site
    if not google_social_app.sites.filter(id=site.id).exists():
        google_social_app.sites.add(site)

    print(f"Google SocialApp configured with Client ID: {google_social_app.client_id}")
