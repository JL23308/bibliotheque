from rest_framework import serializers

from .models import *
from livres.serializers import LivreItemSerializer, UserItemSerializer

class MembreItemSerializer(serializers.Serializer):
    """
        Serializer that transforms a Membre into a JSON response
        Membre (object) => JSON
    """
    user = UserItemSerializer(read_only=True)
    adresse = serializers.CharField(read_only=True)
    telephone = serializers.CharField(read_only=True)
    
class AvisItemSerializer(serializers.Serializer):
    """
        Serializer that transforms an Avis into a JSON response
        Avis (object) => JSON
    """
    note = serializers.IntegerField(read_only=True)
    commentaire = serializers.CharField(read_only=True)

class EmpruntItemSerializer(serializers.Serializer):
    """
        Serializer that transforms an Emprunt into a JSON response
        Emprunt (object) => JSON
    """
    date_emp = serializers.DateField(read_only=True)
    date_ret = serializers.DateField(read_only=True)
    retourne = serializers.DateField(read_only=True)

class EmpruntSerializer(serializers.ModelSerializer):
    membre = MembreItemSerializer(read_only=True)
    livre = LivreItemSerializer(read_only=True)
    class Meta:
        model = Emprunt
        fields = [
            'pk',
            'date_emp',
            'date_ret',
            'retourne',
            'membre',
            'livre'
        ]


class MembreSerializer(serializers.ModelSerializer):
    avis = AvisItemSerializer(read_only=True, many=True)
    emprunt = EmpruntItemSerializer(read_only=True, many=True)
    class Meta:
        model = Membre
        fields = [
            'pk',
            'user',
            'adresse',
            'telephone',
            'avis',
            'emprunt'
        ]

class AvisSerializer(serializers.ModelSerializer):
    membre = MembreItemSerializer(read_only=True)
    livre = LivreItemSerializer(read_only=True)
    class Meta:
        model = Avis
        fields = [
            'pk',
            'note',
            'commentaire',
            'membre',
            'livre',
        ]
