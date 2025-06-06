# managers.py
from django.db import models

class AllObjectsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()