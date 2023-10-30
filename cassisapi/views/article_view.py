"""View for clothing articles."""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from cassisapi.models import Article, Color, Season, Type, Fashionista
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

class ArticleView(ViewSet):
    def create (self, request):
        """Handle POST operations for articles
        Returns:
            Response -- JSON serialized article instance
        """

        parser_classes = (MultiPartParser, FormParser)
        new_article = Article()
        new_article.color = Color.objects.get(pk=request.data["color"])
        new_article.season = Season.objects.get(pk=request.data["season"])
        new_article.type = Type.objects.get(pk=request.data["type"])
        new_article.owner = Fashionista.objects.get(user=request.auth.user)
        new_article.image = request.data["image"]

        new_article.save()

        serializer = ArticleSerializer(new_article, context={'request': request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class ArticleSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    class Meta:
        model = Article
        fields = ('id', 'color', 'season', 'type', 'owner', 'image')
        depth = 1