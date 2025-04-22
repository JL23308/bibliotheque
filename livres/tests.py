from django.test import TestCase
from django.urls import reverse
from .models import * 
from .serializers import *
from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework import status

# Create your tests here.

#===================================================================================
#Model 

class LivreTestCase(TestCase):
    def setUp(self):
        Livre.objects.create(
            titre = 'livre 1',
            date_publication = '2025-04-15',
            isbn = '1234567890777'
        )

        Livre.objects.create(
            titre = 'livre 2',
            date_publication = '2025-04-15',
            isbn = '1234567890778'
        )

        Livre.objects.create(
            titre = 'livre 1',
            date_publication = '2025-04-15',
            isbn = '1234567890779'
        )

        Auteur.objects.create(
            nom = 'S',
            prenom = 'JL',
            date_naissance='2005-07-21'
        )


    def test_isbn_unique(self):
        livre1 = Livre.objects.get(isbn='1234567890777')
        livre2 = Livre.objects.get(isbn='1234567890778')
        livre1.isbn = livre2.isbn
        try:
            livre1.save()
        except:
            livre1.isbn = None
        self.assertIsNone(livre1.isbn)

    def test_isbn_contains_13_digits(self):
        valid = True
        message = ''
        try:
            livre3 = Livre.objects.create(
                titre='titre3',
                date_publication='2025-04-15',
                isbn='29s8d3798a137'
            )
            livre3.full_clean()
            valid = False
            message = 'the isbn contains letter(s)'
        except:
            pass

        try:
            livre4 = Livre.objects.create(
                titre='titre4',
                date_publication='2025-04-15',
                isbn='dazdijaodijaz'
            )
            livre4.full_clean()
            valid = False
            message = 'the isbn contains letters only'
        except:
            pass
        
        try:
            livre5= Livre.objects.create(
                titre='titre5',
                date_publication='2025-04-15',
                isbn='238710398120398230981230283'
            )
            livre5.full_clean()
            valid = False
            message = 'the isbn has over 13 digits'
        except:
            pass

        try:
            livre6= Livre.objects.create(
                titre='titre6',
                date_publication='2025-04-15',
                isbn='123'
            )
            livre6.full_clean()
            valid = False
            message = 'the isbn has bellow 13 digits'
        except:
            pass

        try:
            livre3 = Livre.objects.create(
                titre='titre3',
                date_publication='2025-04-15',
                isbn='1234567890098'
            )
        except:
            valid = False

        self.assertTrue(valid, message)
        
        
    def test_auteur_cant_write_the_same_title_twice(self):
        
        auteur = Auteur.objects.get(pk=1)
        livre1 = Livre.objects.get(isbn='1234567890777')
        livre2 = Livre.objects.get(isbn='1234567890779')

        livre1.auteur = auteur
        livre2.auteur = auteur
        livre1.full_clean()
        livre1.save()
        try:
            livre2.full_clean()
        except:
            livre2.auteur = None
        
        self.assertIsNone(livre2.auteur)
        

    def test_delete_auteur_set_none(self):
        
        auteur = Auteur.objects.get(pk=1)
        livre1 = Livre.objects.get(isbn='1234567890777')
        livre2 = Livre.objects.get(isbn='1234567890778')

        livre1.auteur = auteur
        livre2.auteur = auteur

        livre1.save()
        livre2.save()

        self.assertEqual(livre1.auteur, auteur)
        self.assertEqual(livre2.auteur, auteur)
        
        auteur.delete()
        livre1 = Livre.objects.get(isbn='1234567890777')
        livre2 = Livre.objects.get(isbn='1234567890778')
        
        self.assertIsNone(livre1.auteur)
        self.assertIsNone(livre2.auteur)

class AuteurTestCase(TestCase):
    
    def test_nom_bellow_255_characters(self):
        valid = True
        try:
            auteur = Auteur.objects.create(
                nom="1234123412341234123412341234123412341234123412341234123412341234412341234123412341234123412341234123412341234123412341234123412344123412341234123412341234123412341234123412341234123412341234123444123412341234123412341234123412341234123412341234123441234123412341234123412341234123412341234123412341234123412341234412341234123412341234123412341234123412341234123412341234123412344",
                prenom="1223",
                date_naissance='2025-01-01'
            )
            auteur.full_clean()
            valid = False
        except:
            pass

        try:
            auteur = Auteur.objects.create(
                nom="1234",
                prenom="1223",
                date_naissance='2025-01-01'
            )
            auteur.full_clean()
        except:
            valid = False

        self.assertTrue(valid)

    def test_prenom_bellow_255_characters(self):
        valid = True
        try:
            auteur = Auteur.objects.create(
                nom="1234",
                prenom="1234123412341234123412341234123412341234123412341234123412341234412341234123412341234123412341234123412341234123412341234123412344123412341234123412341234123412341234123412341234123412341234123444123412341234123412341234123412341234123412341234123441234123412341234123412341234123412341234123412341234123412341234412341234123412341234123412341234123412341234123412341234123412344",
                date_naissance='2025-01-01'
            )
            auteur.full_clean()
            valid = False
        except:
            pass

        try:
            auteur = Auteur.objects.create(
                nom="1234",
                prenom="1223",
                date_naissance='2025-01-01'
            )
            auteur.full_clean()
        except:
            valid = False

        self.assertTrue(valid)
        
class CategorieTestCase(TestCase):
    
    def test_nom_bellow_255_characters(self):
        valid = True
        try:
            categorie = Categorie.objects.create(
                nom="1234123412341234123412341234123412341234123412341234123412341234412341234123412341234123412341234123412341234123412341234123412344123412341234123412341234123412341234123412341234123412341234123444123412341234123412341234123412341234123412341234123441234123412341234123412341234123412341234123412341234123412341234412341234123412341234123412341234123412341234123412341234123412344",
                description="1223"
            )
            categorie.full_clean()
            valid = False
        except:
            pass

        try:
            categorie = Categorie.objects.create(
                nom="1234",
                description="1223"
            )
            categorie.full_clean()
        except:
            valid = False

        self.assertTrue(valid)

    def test_description_bellow_255_characters(self):
        valid = True
        try:
            categorie = Categorie.objects.create(
                nom="1234",
                description="1234123412341234123412341234123412341234123412341234123412341234412341234123412341234123412341234123412341234123412341234123412344123412341234123412341234123412341234123412341234123412341234123444123412341234123412341234123412341234123412341234123441234123412341234123412341234123412341234123412341234123412341234412341234123412341234123412341234123412341234123412341234123412344"
            )
            categorie.full_clean()
            valid = False
        except:
            pass

        try:
            categorie = Categorie.objects.create(
                nom="1234",
                description="1223"
            )
            categorie.full_clean()
        except:
            valid = False

        self.assertTrue(valid)


#===================================================================================
#Serializer 

class LivreSerializerTestCase(TestCase):
    def test_is_valid_serializer(self):
        data = {
            'titre': 'titre 1',
            'date_publication': '2025-12-12',
            'isbn': '1234567890098'
        }
        serializer = LivreSerializer(data=data)
        self.assertFalse(serializer.is_valid())

        data = {
            'titre': 'titre 1',
            'date_publication': '2025-01-12',
            'isbn': '1234567890oii'
        }
        serializer = LivreSerializer(data=data)
        self.assertFalse(serializer.is_valid())

        data = {
            'titre': 'titre 1',
            'date_publication': '2025-01-12',
            'isbn': '1234567890111',
        }
        serializer = LivreSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        print(serializer.data)

        data = {
            'titre': 'titre 1',
            'date_publication': 'ajdoiajdioajzd',
            'isbn': '1234567890111',
        }
        serializer = LivreSerializer(data=data)
        self.assertFalse(serializer.is_valid())

#===================================================================================
#API

"""   
class LivreApiTestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(username='admin', password='1234')
        self.normal_user = User.objects.create_user(username='user', password='1234')
        self.livre = (
            Livre.objects.create(
                titre = 'livre 1',
                date_publication = '2025-04-15',
                isbn = '1234567890777'
            ), 
            Livre.objects.create(
                titre = 'livre 2',
                date_publication = '2025-04-15',
                isbn = '1234567890778'
            )
        )
        self.url = reverse('livres')
    
    def test_get_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


    def test_get_list(self):
        print(self.url)
        response = self.client.get(self.url)
        print(response.data)
        self.assertEqual(response.status_code, 200)


    def test_unauthorized_create_product_unauthenticated(self):
        livre = {
            'titre': 'livre 1',
            'date_publication': '2025-04-15',
            'isbn': '1234567890777'
        }

        response = self.client.post(self.url, livre)
        self.assertEqual(response.status_code, 401)
"""