from rest_framework import serializers

from .models import *
from datetime import date
  
from django.utils.translation import gettext_lazy as _
from rest_framework.validators import UniqueTogetherValidator

"""
If we need to display details about Livre in Categorie, Auteur or User

class LivrePublicSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    titre = serializers.CharField(read_only=True)
    date_publication = serializers.DateField(read_only=True)
    isbn = serializers.CharField(read_only=True)

class AuteurPublicSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    prenom = serializers.CharField(read_only=True)
    nom = serializers.CharField(read_only=True)
    date_naissance = serializers.DateField(read_only=True)

class CategoriePublicSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    nom = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)

class UserPublicSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
"""

#============================================

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = '__all__'

class AuteurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auteur
        fields = [
            'pk',
            'prenom',
            'nom',
            'date_naissance',
        ]

class LivreSerializer(serializers.ModelSerializer):
    auteur = AuteurSerializer(read_only=True)
    createur = UserSerializer(read_only=True)
    categorie = CategorieSerializer(read_only=True, many=True)
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

    def validate_date_publication(self, value):
        if value:
            if value > date.today():
                raise serializers.ValidationError(_(str(value) + " is in the future."))
        return value
    
    