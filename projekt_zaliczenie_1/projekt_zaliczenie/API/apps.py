from django.apps import AppConfig
from django.db.models.signals import post_save

class APIConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'API'
    def ready(self):
        from rest_framework.authtoken.models import Token
        from django.contrib.auth import get_user_model
        User = get_user_model()

        from django.db.models.signals import post_save

        def create_auth_token(sender, instance=None, created=False, **kwargs):
            if created:
                Token.objects.create(user=instance)

        post_save.connect(create_auth_token, sender=User)