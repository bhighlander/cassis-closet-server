"""Model for clothing types."""

from django.db import models

class Type(models.Model):
    label = models.CharField(max_length=50)
    owner = models.ForeignKey("Fashionista", on_delete=models.CASCADE)