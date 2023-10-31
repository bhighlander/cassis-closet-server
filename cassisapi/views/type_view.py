"""View module for handling requests about type model"""

from rest_framework import status, serializers
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from cassisapi.models import Type, Fashionista
from django.db.models.functions import Lower

class TypeView(ViewSet):

    def list(self, request):
        """Handle GET requests to type resource

        Returns:
            Response -- JSON serialized list of type
        """

        try:
            type = Type.objects.order_by(Lower('label'))
            serializer = TypeSerializer(Type, many=True, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return Response({'message': ex.args[0]})
        
    def retrieve(self, request, pk=None):
        """Handle GET requests for single type

        Returns:
            Response -- JSON serialized type instance
        """
        try:
            type = Type.objects.get(pk=pk)
            serializer = TypeSerializer(type, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return Response({'message': ex.args[0]})
        
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized type instance
        """
        new_type = Type()
        new_type.label = request.data["label"]
        new_type.owner = Fashionista.objects.get(user=request.auth.user)
        new_type.save()

        serializer = TypeSerializer(new_type, context={'request': request})

        return Response(serializer.data)
    
    def update(self, request, pk=None):
        """Handle PUT requests for a type

        Returns:
            Response -- Empty body with 204 status code
        """
        type = Type.objects.get(pk=pk)
        type.label = request.data["label"]
        type.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single type

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            type = Type.objects.get(pk=pk)
            type.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Type.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class TypeSerializer(serializers.ModelSerializer):
    """JSON serializer for type

    Arguments:
        serializer type
    """
    class Meta:
        model = Type
        fields = ('id', 'label')
        depth = 1