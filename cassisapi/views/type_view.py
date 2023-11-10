"""View module for handling requests about clothing_type model"""

from rest_framework import status, serializers
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from cassisapi.models import Type, Fashionista
from django.db.models.functions import Lower

class TypeView(ViewSet):

    def list(self, request):
        """Handle GET requests to clothing_type resource

        Returns:
            Response -- JSON serialized list of clothing_type
        """

        try:
            fashionista = Fashionista.objects.get(user=request.auth.user)
            clothing_type= Type.objects.order_by(Lower('label')).filter(owner=fashionista)
            serializer = TypeSerializer(clothing_type, many=True, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return Response({'message': ex.args[0]})
        
    def retrieve(self, request, pk=None):
        """Handle GET requests for single clothing_type

        Returns:
            Response -- JSON serialized clothing_type instance
        """
        try:
            clothing_type = Type.objects.get(pk=pk)
            serializer = TypeSerializer(clothing_type, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return Response({'message': ex.args[0]})
        
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized clothing_type instance
        """
        new_clothing_type = Type()
        new_clothing_type.label = request.data["label"]
        new_clothing_type.owner = Fashionista.objects.get(user=request.auth.user)
        new_clothing_type.save()

        serializer = TypeSerializer(new_clothing_type, context={'request': request})

        return Response(serializer.data)
    
    def update(self, request, pk=None):
        """Handle PUT requests for a clothing_type

        Returns:
            Response -- Empty body with 204 status code
        """
        clothing_type = Type.objects.get(pk=pk)
        clothing_type.label = request.data["label"]
        clothing_type.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single clothing_type

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            clothing_type = Type.objects.get(pk=pk)
            clothing_type.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Type.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class TypeSerializer(serializers.ModelSerializer):
    """JSON serializer for clothing_type

    Arguments:
        serializer clothing_type
    """
    class Meta:
        model = Type
        fields = ('id', 'label')
        depth = 1