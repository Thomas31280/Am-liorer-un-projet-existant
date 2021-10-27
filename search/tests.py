from django.test import TestCase, Client, LiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

from search.models import Aliment, Category

############################
#########Unit Tests#########
############################


class SearchTestCase(TestCase):

    # INDEX

    # test that index returns a 200
    def test_index(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    # INFO_ALIMENT

    # test that info_aliment returns a 200
    def test_info_aliment(self):
        c = Client()                                                             # On créé une instance de la classe client
        Category.objects.create(category="Category test")                        # On "mock" une nouvelle categorie ( terme largement abusif, car on la créé bel et bien sans la save ) pour le test unitaire
        aliment_category = Category.objects.get(category="Category test")        # On récupère l'instance ainsi créée
        Aliment.objects.create(product_name='Produit Test',
                               pnns_groups_1=aliment_category,
                               url="https://test", nutriscore="e",
                               img_url="https://test.fr")                        # On applique la même démarche avec une instance de la table aliment, pour laquelle on va se servir de l'instance précédemment créée
        url = Aliment.objects.get(product_name='Produit Test').url               # On récupère l'url de l'aliment en question
        response = c.get('/aliment/', {'query': url})                            # On utilise la méthode get sur l'instance Client pour générer une requête de verbe HTTP GET sur le schéma d'URL /aliment/ avec pour paramètre query = url
        self.assertEqual(response.status_code, 200)                              # On attends une réponse 200 du serveur

    # SEARCH_SUBSTITUTE

    # test that search_substitutes returns a 200 if the URL parameters match with an element in aliment table
    def test_search_substitute_success(self):
        c = Client()
        Category.objects.create(category="Category test")
        aliment_category = Category.objects.get(category="Category test")
        Aliment.objects.create(product_name='Produit Test',
                               pnns_groups_1=aliment_category,
                               url="https://test", nutriscore="e",
                               img_url="https://test.fr")
        Aliment.objects.create(product_name='Produit Test_2',
                               pnns_groups_1=aliment_category,
                               url="https://test_2",
                               nutriscore="a", img_url="https://test.fr_2")
        product_name = Aliment.objects.get(product_name='Produit Test').product_name
        response = c.get('/result/', {'query': product_name})
        self.assertEqual(response.status_code, 200)

    # test that search_substitutes returns a 500 if the URL parameters doesn't match with any element in aliment table
    def test_search_substitute_fail(self):
        c = Client()
        product_name = "produit_non_répertorié_en_base"
        response = c.get('/result/', {'query': product_name})
        self.assertEqual(response.status_code, 500)


################################
#########Selenium Tests#########
################################

class UserTest(LiveServerTestCase):

    # Test the following pattern : User consult the main page, logout, click on the icon of connexion page, enter his
    # personnal informations in the inputfields, click on "se connecter" and click again on the icon of connexion page
    def test_consult_favorites(self):

        selenium = webdriver.Chrome(ChromeDriverManager().install())

        selenium.get('http://127.0.0.1:8000/')                       # Choose the url to visit

        # Find the elements we need in the page
        logout = selenium.find_element_by_id('logout')

        # Click on logout
        logout.click()

        selenium.get('http://127.0.0.1:8000/compte/')

        submit = selenium.find_element_by_id('connexion')
        inputfield_mail = selenium.find_element_by_id('mail')
        inputfield_username = selenium.find_element_by_id('userName')

        # Populate the form with data
        inputfield_mail.send_keys('johndoe@hotmail.fr')
        inputfield_username.send_keys('Bruce_Wayne')

        # Submit form
        submit.send_keys(Keys.RETURN)

        selenium.get('http://127.0.0.1:8000/compte/')

        # Check result; page source looks at entire html document
        assert 'Bruce_Wayne' in selenium.page_source
