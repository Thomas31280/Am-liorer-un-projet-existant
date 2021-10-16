from django.test import TestCase, Client
from django.urls import reverse

from search.models import Aliment, Category

class SearchTestCase(TestCase):

    # Index

        # test that index returns a 200
    def test_index(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)


    # Info_aliment
        # test that info_aliment returns a 200
    def test_info_aliment(self):
        c = Client()                                                             # On créé une instance de la classe client
        Category.objects.create(category="Category test")                        # On "mock" une nouvelle categorie ( terme largement abusif, car on la créé bel et bien sans la save ) pour le test unitaire
        aliment_category = Category.objects.get(category="Category test")        # On récupère l'instance ainsi créée
        Aliment.objects.create(product_name='Produit Test', pnns_groups_1=aliment_category, url="https://test", nutriscore="e", img_url="https://test.fr") # On applique la même démarche avec une instance de la table aliment, pour laquelle on va se servir de l'instance précédemment créée
        url = Aliment.objects.get(product_name='Produit Test').url               # On récupère l'url de l'aliment en question
        response = c.get('/aliment/', {'query': url})                            # On utilise la méthode get sur l'instance Client pour générer une requête de verbe HTTP GET sur le schéma d'URL /aliment/ avec pour paramètre query = url
        self.assertEqual(response.status_code, 200)                              # On attends une réponse 200 du serveur


    # Search_substitute
        # test that search_substitutes returns a 200 if the URL parameters match with an element in aliment table
    def test_search_substitute_success(self):
        c = Client()
        Category.objects.create(category="Category test")
        aliment_category = Category.objects.get(category="Category test")
        Aliment.objects.create(product_name='Produit Test', pnns_groups_1=aliment_category, url="https://test", nutriscore="e", img_url="https://test.fr")
        Aliment.objects.create(product_name='Produit Test_2', pnns_groups_1=aliment_category, url="https://test_2", nutriscore="a", img_url="https://test.fr_2")
        product_name = Aliment.objects.get(product_name='Produit Test').product_name
        response = c.get('/result/', {'query': product_name})
        self.assertEqual(response.status_code, 200)

        # test that search_substitutes returns a 500 if the URL parameters doesn't match with any element in aliment table
    def test_search_substitute_fail(self):
        c = Client()
        product_name = "produit_non_répertorié_en_base"
        response = c.get('/result/', {'query': product_name})
        self.assertEqual(response.status_code, 500)