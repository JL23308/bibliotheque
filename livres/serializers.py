from rest_framework import serializers

from .models import *
from datetime import date
  
from django.utils.translation import gettext_lazy as _
from rest_framework.validators import UniqueTogetherValidator

class LivreItemSerializer(serializers.Serializer):
    """
        Serializer that transforms a Livre to a JSON format
        Livre (Object) => JSON
    """
    pk = serializers.IntegerField(read_only=True)
    titre = serializers.CharField(read_only=True)
    date_publication = serializers.DateField(read_only=True)
    isbn = serializers.CharField(read_only=True)

class AuteurItemSerializer(serializers.Serializer):
    """
        Serializer that transforms an Auteur to a JSON format
        Auteur (Object) => JSON
    """
    pk = serializers.IntegerField(read_only=True)
    prenom = serializers.CharField(read_only=True)
    nom = serializers.CharField(read_only=True)
    date_naissance = serializers.DateField(read_only=True)

class CategorieItemSerializer(serializers.Serializer):
    """
        Serializer that transforms a Categorie to a JSON format
        Categorie (Object) => JSON
    """
    pk = serializers.IntegerField(read_only=True)
    nom = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)

class UserItemSerializer(serializers.Serializer):
    """
        Serializer that transforms a User to a JSON format
        User (Object) => JSON
    """
    pk = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)


#============================================

class UserSerializer(serializers.ModelSerializer):
    """
        Serializer that transforms data passed in a request into a Users 
        JSON => User (Object)
    """
    class Meta:
        model = User
        fields = '__all__'

class CategorieSerializer(serializers.ModelSerializer):
    """
        Serializer that transforms data passed in a request into a Categorie 
        JSON => Categorie (Object)
    """
    class Meta:
        model = Categorie
        fields = '__all__'

class AuteurSerializer(serializers.ModelSerializer):
    """
        Serializer that transforms data passed in a request into an Auteur 
        JSON => Auteur (Object)
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
        Serializer that transforms data passed in a request into a Livre 
        JSON => Livre (Object)
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
        function that calls when is_valid() function is called.
        Verifies if the date if not from the future
    """
    def validate_date_publication(self, value):
        if value:
            if value > date.today():
                raise serializers.ValidationError(_(str(value) + " is in the future."))
        return value
    
    