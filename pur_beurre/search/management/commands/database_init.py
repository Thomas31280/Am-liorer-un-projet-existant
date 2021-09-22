###########################################################
###Création d'une nouvelle commande personnalisée Django###
###########################################################

from django.core.management.base import BaseCommand                                  # On importe le module Django BaseCommand
import http_request

from search.models import Aliment
from search.models import Category


class Command(BaseCommand):                                                          # On définit une nouvelle classe qui hérite de BaseCommand
    args = '<team_id>'
    help = "Permet d'initialiser la table Aliment de la DB avec l'API OpenFoodFacts" # On définit une chaine d'aide pour notre commande personnalisée (python manage.py command --help)

    def handle(self, *args, **options):                                              # La méthode handle va implémenter le code exécuté par la commande personnalisée
        with open("html_requests.txt") as instruction:                               # On récupère les URL dans html_requests.txt
                
                for line in instruction.readlines():
                    result = http_request.Requests.get_data_from_api(line)           # On réalise nos appels à l'API OFF avec le module http_request
                    
                    for product in result["products"]:                               # Récupération des données produits dans les JSON
                        
                        try:
                            url = product["url"]
                            category = product["pnns_groups_1"]
                            name = product["product_name"]
                            nutriscore = product["nutriscore_grade"]
                            
                            try:
                                new_row_category = Category(category=category)       # On commence par insérer la categorie du produit dans la table category, qui a une contrainte d'unicité sur son champ category, puis on sauvegarde
                                print("Ceci est une nouvelle catégorie : ", new_row_category)
                                new_row_category.save()
                            except:
                                pass
                            
                            product_category = Category.objects.get(category=category)                 # On va chercher l'objet qui correspond à la catégorie dans la table category, afin de pouvoir le lier à l'instance de la table aliment
                            print("Ceci est mon produit de la table catégorie : ", product_category)
                            
                            try:
                                print("Je suis arrivé jusque là...")
                                new_row_aliment = Aliment(pnns_groups_1=product_category, product_name=name, nutriscore=nutriscore, url=url) # On insère les données dans la table Aliment, puis on sauvegarde les modifications après chaque insertion
                                print("Ceci est mon instance de la table Aliment : ", new_row_aliment)
                                new_row_aliment.save()

                                print("Ok")
                            except:
                                print("A problem occured !!")
                        
                        except:
                            pass

                print("Database successfully initialized")
