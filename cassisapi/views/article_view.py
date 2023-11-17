"""View for clothing articles."""
from datetime import datetime
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from cassisapi.models import Article, Color, Type, Fashionista

class ArticleView(ViewSet):
    parser_classes = (MultiPartParser, FormParser)
    def create (self, request):
        """Handle POST operations for articles
        Returns:
            Response -- JSON serialized article instance
        """

        new_article = Article()
        new_article.color = Color.objects.get(pk=request.data["color"])
        new_article.season = request.data["season"]
        new_article.type = Type.objects.get(pk=request.data["type"])
        new_article.owner = Fashionista.objects.get(user=request.auth.user)
        new_article.image = request.data["image"]
        new_article.last_edited = datetime.now()

        new_article.save()

        serializer = ArticleSerializer(new_article, context={'request': request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def list(self, request):
        """Handle GET requests to articles resource
        Returns:
            Response -- JSON serialized list of articles
        """
        try:
            articles = Article.objects.order_by('-last_edited')
            fashionista = Fashionista.objects.get(user=request.auth.user)
            articles = articles.filter(owner=fashionista)
            serializer = ArticleSerializer(articles, many=True, context={'request': request})
            return Response(serializer.data)

        except Article.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
    def retrieve(self, request, pk=None):
        """Handle GET requests for single article
        Returns:
            Response -- JSON serialized article instance
        """
        try:
            article = Article.objects.get(pk=pk)
            serializer = ArticleSerializer(article, context={'request': request})
            return Response(serializer.data)
        except Article.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single article
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            article = Article.objects.get(pk=pk)
            article.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Article.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
    def update(self, request, pk=None):
        """Handle PUT requests for an article
        Returns:
            Response -- Empty body with 204 status code
        """
        article = Article.objects.get(pk=pk)
        article.color = Color.objects.get(pk=request.data["color"])
        article.season = request.data["season"]
        article.type = Type.objects.get(pk=request.data["type"])
        article.last_edited = datetime.now()
        if 'image' in request.FILES and request.data["image"] != None:
            article.image = request.FILES["image"]

        article.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

class ArticleSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    class Meta:
        model = Article
        fields = ('id', 'color', 'season', 'type', 'owner', 'image', 'last_edited')
        depth = 1