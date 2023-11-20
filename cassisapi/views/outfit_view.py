"""View for outfits."""
from datetime import datetime
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from cassisapi.models import Outfit, Fashionista, Article, Color

class OutfitView(ViewSet):
    def create(self, request):
        """Handle POST operations for outfits
        Returns:
            Response -- JSON serialized outfit instance
        """
        new_outfit = Outfit()
        new_outfit.owner = Fashionista.objects.get(user=request.auth.user)
        new_outfit.color = Color.objects.get(pk=request.data["color"])
        new_outfit.season = request.data["season"]
        new_outfit.last_edited = datetime.now()
        new_outfit.save()
        selected_articles = request.data.get('articles', [])
        new_outfit.articles.set(selected_articles)

        serializer = OutfitSerializer(new_outfit, context={'request': request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
class OutfitSerializer(serializers.ModelSerializer):
    """JSON serializer for outfits
    Arguments:
        serializer type
    """
    class Meta:
        model = Outfit
        fields = ('id', 'owner', 'color', 'season', 'articles', 'last_edited')
        depth = 1
