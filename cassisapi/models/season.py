"""Model for clothing seasons."""

from django.db import models

class Season(models.Model):
    label = models.CharField(max_length=50)