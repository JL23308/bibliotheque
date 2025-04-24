from rest_framework import serializers

from .models import *
from datetime import date
  
from django.utils.translation import gettext_lazy as _
from rest_framework.validators import UniqueTogetherValidator

class LivreItemSerializer(serializers.Serializer):
    """
        Serializer that transforms a Livre into a JSON response
        Livre (object) => JSON
    """
    pk = serializers.IntegerField(read_only=True)
    titre = serializers.CharField(read_only=True)
    date_publication = serializers.DateField(read_only=True)
    isbn = serializers.CharField(read_only=True)

class AuteurItemSerializer(serializers.Serializer):
    """
        Serializer that transforms an Auteur into a JSON response
        Auteur (object) => JSON
    """
    pk = serializers.IntegerField(read_only=True)
    prenom = serializers.CharField(read_only=True)
    nom = serializers.CharField(read_only=True)
    date_naissance = serializers.DateField(read_only=True)

class CategorieItemSerializer(serializers.Serializer):
    """
        Serializer that transforms a Categorie into a JSON response
        Categorie (object) => JSON
    """
    pk = serializers.IntegerField(read_only=True)
    nom = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)

class UserItemSerializer(serializers.Serializer):
    """
        Serializer that transforms an User into a JSON response
        User (object) => JSON
    """
    pk = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)


#============================================

class UserSerializer(serializers.ModelSerializer):
    """
        Serializer that transforms data passed into an User
        JSON, form => User (object)
    """
    class Meta:
        model = User
        fields = '__all__'

class CategorieSerializer(serializers.ModelSerializer):
    """
        Serializer that transforms data passed into a Categorie
        JSON, form => Categorie (object)
    """
    class Meta:
        model = Categorie
        fields = '__all__'

class AuteurSerializer(serializers.ModelSerializer):
    """
        Serializer that transforms data passed into an Auteur
        JSON, form => Auteur (object)
    """
    class Meta:
        model = Auteur
        fields = [
            'pk',
            'prenom',
            'nom',
            'date_naissance',
        ]

class LivreSerializer(serializers.ModelSerializer):
    """
        Serializer that transforms data passed into a Livre
        JSON, form => Livre (object)
    """
    auteur = AuteurItemSerializer(read_only=True)
    createur = UserItemSerializer(read_only=True)
    categorie = CategorieItemSerializer(read_only=True, many=True)
    class Meta:
        model = Livre
        fields = [
            'pk',
            'titre',
            'auteur',
            'date_publication',
            'isbn',
            'createur',
            'categorie'
        ]

    """
        Function that checks if a date is valid.
        
        param: 
            - date value
        return:
            date or error

        example: 
        today : 2025-04-23
        2025-01-01 => 2025-01-01
        2026-01-01 => ValidationError
    """
    def validate_date_publication(self, value):
        if value:
            if value > date.today():
                raise serializers.ValidationError(_(str(value) + " is in the future."))
        return value
    
    