"""View module for handling requests about color model"""

from rest_framework import status, serializers
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from cassisapi.models import Color, Fashionista
from django.db.models.functions import Lower

class ColorView(ViewSet):

    def list(self, request):
        """Handle GET requests to color resource

        Returns:
            Response -- JSON serialized list of color
        """

        try:
            fashionista = Fashionista.objects.get(user=request.auth.user)
            color = Color.objects.order_by(Lower('label')).filter(owner=fashionista)
            serializer = ColorSerializer(color, many=True, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return Response({'message': ex.args[0]})
        
    def retrieve(self, request, pk=None):
        """Handle GET requests for single color

        Returns:
            Response -- JSON serialized color instance
        """
        try:
            color = Color.objects.get(pk=pk)
            serializer = ColorSerializer(color, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return Response({'message': ex.args[0]})
        
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized color instance
        """
        new_color = Color()
        new_color.label = request.data["label"]
        new_color.owner = Fashionista.objects.get(user=request.auth.user)
        new_color.save()

        serializer = ColorSerializer(new_color, context={'request': request})

        return Response(serializer.data)
    
    def update(self, request, pk=None):
        """Handle PUT requests for a color

        Returns:
            Response -- Empty body with 204 status code
        """
        color = Color.objects.get(pk=pk)
        color.label = request.data["label"]
        color.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single color

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            color = Color.objects.get(pk=pk)
            color.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Color.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ColorSerializer(serializers.ModelSerializer):
    """JSON serializer for color

    Arguments:
        serializer type
    """
    class Meta:
        model = Color
        fields = ('id', 'label')
        depth = 1