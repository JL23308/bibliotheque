from django.test import TestCase
from django.urls import reverse
from .models import * 
from .serializers import *
from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

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

        data = {
            'titre': 'titre 1',
            'date_publication': 'ajdoiajdioajzd',
            'isbn': '1234567890111',
        }
        serializer = LivreSerializer(data=data)
        self.assertFalse(serializer.is_valid())

#===================================================================================
#API


class LivreApiTestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(username='admin', password='1234')
        self.normal_user = User.objects.create_user(username='user', password='1234')

        self.auteurs = [
            Auteur.objects.create(nom='Sithi', prenom='Jean-Luck'),
            Auteur.objects.create(nom='Perosino', prenom='Cyril', date_naissance='1998-12-20')
        ]
        
        self.categories = [
            Categorie.objects.create(nom='Aventure', description='voyage'),
            Categorie.objects.create(nom='Horreur', description='fait peur'),
            Categorie.objects.create(nom='Fantaisie', description='monde imaginaire'),     
        ]

        self.livres = [
            Livre.objects.create(
                titre="titre1", 
                date_publication="2025-04-01", 
                isbn="1234567890098",
                createur=self.admin_user,
                auteur=self.auteurs[0],
            ),
            Livre.objects.create(
                titre="titre2", 
                isbn="1234567890093",
                createur=self.normal_user,
                auteur=self.auteurs[1]
            ),
            Livre.objects.create(
                titre="titre3", 
                date_publication="2025-07-21", 
                isbn="1234567890099",
                createur=self.admin_user,
                auteur=self.auteurs[0]
            ),
            Livre.objects.create(
                titre="titre4", 
                isbn="1234567890090",
                createur=self.normal_user,
                auteur=self.auteurs[1]
            ),
        ]

        self.livres[0].categorie.add(self.categories[0], self.categories[2])
        self.livres[1].categorie.add(self.categories[1])
        self.livres[2].categorie.add(self.categories[1], self.categories[2])
        self.livres[3].categorie.add(self.categories[0], self.categories[1], self.categories[2])


    def test_get_list_unauthenticated(self):
        url = reverse('livres:livres-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 4)

    def test_get_livre_unauthenticated(self):
        url = reverse('livres:livres-detail', kwargs={'pk':1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['titre'], "titre1")
        self.assertEqual(response.data['date_publication'], "2025-04-01")
        self.assertEqual(response.data['isbn'], "1234567890098")
        self.assertEqual(response.data['auteur']['pk'], self.auteurs[0].pk)
    
    def authenticate(self):
        url = reverse('token-auth')
        user_data = {
            'username': 'admin',
            'password': 1234
        }
        token = self.client.post(url, user_data)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.data['token'])

    def test_create_livre(self):   
        self.authenticate()
        url = reverse('livres:livres-list')
        livre_data = {
            'titre': 'new livre',
            'date_publication': '2025-01-01',
            'isbn': '7876789098765',
        }
        
        response = self.client.post(url, livre_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['titre'], 'new livre')
        self.assertEqual(response.data['date_publication'], '2025-01-01')
        self.assertEqual(response.data['isbn'], '7876789098765')
      
        
    def test_edit_livre(self):
        self.authenticate()
        url = reverse('livres:livres-detail', kwargs={'pk': 1})
        livre_data = {
            'titre': 'new livre'
        }
        response = self.client.patch(url, livre_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['titre'], 'new livre')
        self.assertEqual(response.data['date_publication'], '2025-04-01')
        self.assertEqual(response.data['isbn'], '1234567890098')

        livre_data = {
            'titre': 'new livre 2',
            'date_publication': None,
            'isbn': '2283729837297',
        }

        response = self.client.put(url, livre_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['titre'], 'new livre 2')
        self.assertIsNone(response.data['date_publication'])
        self.assertEqual(response.data['isbn'], '2283729837297')
        

    def test_delete_livre(self):
        self.authenticate()
        url = reverse('livres:livres-detail', kwargs={'pk': 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        
    def test_filter(self):
        url = reverse('livres:livres-list', query={'titre': '1'})
        response = self.client.get(url)
        self.assertEqual(len(response.data['results']), 1)
        
        url = reverse('livres:livres-list', query={'titre': 'titre'})
        response = self.client.get(url)
        self.assertEqual(len(response.data['results']), 3)

        url = reverse('livres:livres-list', query={
            'titre': 'titre3', 
            'date_publication_min': '2025-04-01',
            'date_publication_max': '2025-04-01',
            })
        response = self.client.get(url)
        self.assertEqual(len(response.data['results']), 0)

        url = reverse('livres:livres-list', query={
            'categorie_nom': 'horreur'
            })
        response = self.client.get(url)
        self.assertEqual(len(response.data['results']), 3)


        url = reverse('livres:livres-list', query={
            'categorie_nom': 'HorREur'
            })
        response = self.client.get(url)
        self.assertEqual(len(response.data['results']), 3)

        url = reverse('livres:livres-list', query={
            'ordering': 'titre'
            })
        response = self.client.get(url)
        self.assertEqual(response.data['results'][0]['titre'], 'titre1')

        url = reverse('livres:livres-list', query={
            'ordering': '-titre'
            })
        response = self.client.get(url)
        self.assertEqual(response.data['results'][0]['titre'], 'titre4')

        url = reverse('livres:livres-list', query={
            'ordering': 'date_publication'
            })
        response = self.client.get(url)
        self.assertIsNone(response.data['results'][0]['date_publication'])

        url = reverse('livres:livres-list', query={
            'ordering': '-date_publication'
            })
        response = self.client.get(url)
        self.assertEqual(response.data['results'][0]['date_publication'], '2025-07-21')


    def test_pagination(self):
        pass
    
    def test_permissions(self):
        pass
    
    