from rest_framework import serializers
from core.models import Author

class AuthorSerializer( serializers.Serializer ):
    id = serializers.IntegerField( read_only=True )
    name = serializers.CharField( max_length=255 )
