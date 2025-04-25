from django.db import models
from livres.models import Livre, User

# Create your models here.

class Membre(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    adresse = models.CharField(max_length=255, blank=True, null=True)
    telephone = models.CharField(max_length=10, blank=True, null=True)
    
class Avis(models.Model):
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE, blank=True, null=True)
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE, blank=True, null=True)
    note = models.IntegerField(blank=True, null=True)
    commentaire = models.CharField(max_length=5000, blank=True, null=True)

class Emprunt(models.Model):
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE, blank=True, null=True)
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE, blank=True, null=True)
    date_emp = models.DateField(blank=True, null=True, max_length=10)
    date_ret = models.DateField(blank=True, null=True, max_length=10)
    retourne = models.DateField(blank=True, null=True)