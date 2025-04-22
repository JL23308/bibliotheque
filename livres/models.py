from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

#validators

def validate_isbn(value):
    if len(value) != 13:
        raise ValidationError(_("%(value)s size is not correct."), params={"value": value})
    
    if not value.isdigit():
        raise ValidationError(_("%(value)s is incorrect. It must contain numbers only"), params={"value": value})

# Create your models here.

class Auteur(models.Model):
    nom = models.CharField(max_length=255, null=True, blank=True)
    prenom = models.CharField(max_length=255, null=True, blank=True)
    date_naissance = models.DateField(null=True, blank=True)

class Categorie(models.Model):
    nom = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)

class Livre(models.Model):
    titre = models.CharField(max_length=255, null=True, blank=True)
    auteur = models.ForeignKey(Auteur, on_delete=models.SET_NULL, null=True, blank=True)
    date_publication = models.DateField(max_length=255, null=True, blank=True)
    isbn = models.CharField(max_length=13, null=True, blank=True, unique=True, validators=[validate_isbn])
    createur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    categorie = models.ManyToManyField(Categorie, related_name='livre', null=True, blank=True)

    def clean(self):
        errors = {}
        double = Livre.objects.filter(titre=self.titre, auteur=self.auteur)
        if double:
            errors['titre'] = ValidationError(_("This author already used this title."))

        if errors:
            raise ValidationError(errors)
    
        super().clean()
        