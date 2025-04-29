from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

#validators

def validate_isbn(value):
    if len(value) != 13:
        raise ValidationError(_("%(value)s size is not correct."), params={"value": value})
    
    if not value.isdigit():
        raise ValidationError(_("%(value)s is incorrect. It must contain numbers only"), params={"value": value})

# Create your models here.
  
class Auteur(models.Model):
    """
        Model that describes an author.
        An author is related to many books (Livre)
    """
    nom = models.CharField(max_length=255, null=True, blank=True)
    prenom = models.CharField(max_length=255, null=True, blank=True)
    date_naissance = models.DateField(null=True, blank=True)

class Categorie(models.Model):
    """
        Model that describes an category.
        A categorie is related to many books (Livre)
    """
    nom = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)

class Livre(models.Model):
    """
        Model that describes an category.
        A categorie is related to many books (Livre)
    """
    titre = models.CharField(max_length=255, null=True, blank=True)
    auteur = models.ForeignKey(Auteur, on_delete=models.SET_NULL, null=True, blank=True)
    date_publication = models.DateField(max_length=255, null=True, blank=True)
    isbn = models.CharField(max_length=13, null=True, blank=True, unique=True, validators=[validate_isbn])
    createur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    categorie = models.ManyToManyField(Categorie, related_name='livre', null=True, blank=True)

    def clean(self):
        errors = {}
        try:
            exists = Livre.objects.get(pk=self.id)
            double = Livre.objects.filter(titre=self.titre, auteur=self.auteur).exclude(id=exists.id)
        except:
            double = None
        if double:
            errors['titre'] = ValidationError(_("This author already used this title."))
        if errors:
            raise ValidationError(errors)
    
        super().clean()
    
    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Livre, self).save(*args, **kwargs)
