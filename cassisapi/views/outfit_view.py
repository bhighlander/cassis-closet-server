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
        selected_articles_ids = request.data.get('articles', [])
        selected_articles_instances = Article.objects.filter(id__in=selected_articles_ids)
        new_outfit.articles.set(selected_articles_instances)

        serializer = OutfitSerializer(new_outfit, context={'request': request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def list(self, request):
        """Handle GET requests to outfits resource
        Returns:
            Response -- JSON serialized list of outfits
        """
        fashionista = Fashionista.objects.get(user=request.auth.user)
        outfits = Outfit.objects.filter(owner=fashionista)
        serializer = OutfitSerializer(
            outfits, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        """Handle GET requests for single outfit
        Returns:
            Response -- JSON serialized outfit instance
        """
        try:
            outfit = Outfit.objects.get(pk=pk)
            serializer = OutfitSerializer(outfit, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({'message': ex.args[0]})
        
class OutfitSerializer(serializers.ModelSerializer):
    """JSON serializer for outfits
    Arguments:
        serializer type
    """
    class Meta:
        model = Outfit
        fields = ('id', 'owner', 'color', 'season', 'articles', 'last_edited')
        depth = 1
