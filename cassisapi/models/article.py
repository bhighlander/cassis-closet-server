"""Model for clothing articles."""

from django.db import models

class Article(models.Model):
    color = models.ForeignKey("Color", on_delete=models.CASCADE)
    season = models.ForeignKey("Season", on_delete=models.CASCADE)
    type = models.ForeignKey("Type", on_delete=models.CASCADE)
    owner = models.ForeignKey("Fashionista", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', height_field=None, null=True, blank=True)