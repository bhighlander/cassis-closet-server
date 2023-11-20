"""Model for outfit."""

from django.db import models

class Outfit(models.Model):
    owner = models.ForeignKey("Fashionista", on_delete=models.CASCADE)
    color = models.ForeignKey("Color", on_delete=models.CASCADE)
    season = models.CharField(max_length=6)
    articles = models.ManyToManyField("Article", through="OutfitArticle")
    last_edited = models.DateTimeField(auto_now=True)