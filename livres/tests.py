from django.test import TestCase
from django.urls import reverse
from .models import * 
from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework import status

# Create your tests here.

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

    def test_auteur(self):
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