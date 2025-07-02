from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from spodcat.model_mixin import ModelMixin


class User(ModelMixin, AbstractUser):
    language = models.CharField(max_length=10, choices=settings.LANGUAGES, null=True, default=None)

    def has_change_permission(self, request):
        return request.user.is_superuser or request.user == self
