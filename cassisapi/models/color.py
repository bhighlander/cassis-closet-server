"""Model for clothing colors."""

from django.db import models

class Color(models.Model):
    label = models.CharField(max_length=50)
    owner = models.ForeignKey("Fashionista", on_delete=models.CASCADE)