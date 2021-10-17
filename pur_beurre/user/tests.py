from django.test import TestCase, Client
from django.urls import reverse

from search.models import Aliment, Category, Favorites
from django.contrib.auth.models import User

class UserTestCase(TestCase):

    # Account_page
        # test that account_page returns a 200
    def test_account_page(self):
        response = self.client.get(reverse('compte'))
        self.assertEqual(response.status_code, 200)


    # create_account
        # test that create_account returns a 200 if the URL parameters exist and are valids
    def test_create_account_success(self):
        c = Client()
        username = "Jonh_Doe"
        email = "test@bidon.fr"
        response = c.get('/create/', {'username': username, "email": email})
        self.assertEqual(response.status_code, 200)

        # test that create_account returns a 500 if the URL parameters doesn't exist or aren't valids
    def test_create_account_fail(self):
        c = Client()
        username = "Jonh_Doe"
        email = ""
        response = c.get('/create/', {'username': username, "email": email})
        self.assertEqual(response.status_code, 500)


    # connect_account
        # test that connect_account returns a 200 if the URL parameters match with an element in user table
    def test_login_success(self):
        c = Client()
        username = "John Doe"
        email = "john@doe.baniou"
        User.objects.create(username=username, email=email)
        response = c.get('/connect/', {'username': username, 'email': email})
        self.assertEqual(response.status_code, 200)

        # test that connect_account returns a 500 if the URL parameters doesn't match with any user in aliment table
    def test_login_fail(self):
        c = Client()
        username = "John Doe"
        email = "john@doe.baniou"
        response = c.get('/connect/', {'username': username, 'email': email})
        self.assertEqual(response.status_code, 500)    


    # disconnect_account
        # test that diconnect_account returns a 200
    def test_logout(self):
        response = self.client.get(reverse('disconnect'))
        self.assertEqual(response.status_code, 200)


    # add_product_to_favorites
        # test that add_product_to_favorites returns a 200 if the user is connected and the product isn't in his favorites
    def test_add_product_to_favorites(self):
        c = Client()
        
        category = Category.objects.create(category="Category test")
        
        username = "John Doe"
        email = "monmail@legit.fr"
        
        user = User.objects.create(username=username, email=email)
        c.get('/connect/', {'username': username, "email": email})

        url = "https://test"
        product_name = 'Produit Test'
        img_url = "https://test.fr"
        
        Aliment.objects.create(product_name=product_name, pnns_groups_1=category, url=url, nutriscore="e", img_url=img_url)
        
        response = c.get('/add_product/', {'url': url})
        self.assertEqual(response.status_code, 200)

        # test that add_product_to_favorites returns a 500 if the user is connected and the product already is in his favorites
    def test_add_two_times_product_to_favorites(self):
        c = Client()
        
        category = Category.objects.create(category="Category test")
        
        username = "John Doe"
        email = "monmail@legit.fr"
        
        user = User.objects.create(username=username, email=email)
        c.get('/connect/', {'username': username, "email": email})

        url = "https://test"
        product_name = 'Produit Test'
        img_url = "https://test.fr"
        
        aliment = Aliment.objects.create(product_name=product_name, pnns_groups_1=category, url=url, nutriscore="e", img_url=img_url)
        Favorites.objects.create(product_id=aliment, user_id=user)
        
        response = c.get('/add_product/', {'url': url})
        self.assertEqual(response.status_code, 500)

        # test that add_product_to_favorites returns a 500 if the user isn't connected
    def test_add_product_to_favorites_offline(self):
        c = Client()
        c.get('/disconnect/')

        category = Category.objects.create(category="Category test")

        url = "https://test"
        product_name = 'Produit Test'
        img_url = "https://test.fr"
        
        aliment = Aliment.objects.create(product_name=product_name, pnns_groups_1=category, url=url, nutriscore="e", img_url=img_url)
        
        response = c.get('/add_product/', {'url': url})
        self.assertEqual(response.status_code, 500)


    # consult_favorites
        # test that consult_favorites returns a 200 if the user is connected
    def test_consult_favorites(self):
        c = Client()
        
        username = "Nom random"
        email = "Jonny@hotmail.fr"
        User.objects.create(username=username, email=email)
        
        c.get('/connect/', {'username': username, "email": email})
        
        response = c.get('/my_favorites/')
        self.assertEqual(response.status_code, 200)
        
        # test that consult_favorites returns a 500 if the user isn't connected
    def test_consult_favorites_offline(self):
        c = Client()
        response = c.get('/my_favorites/')
        self.assertEqual(response.status_code, 500)
