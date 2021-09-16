###########################################################
###Création d'une nouvelle commande personnalisée Django###
###########################################################

from django.core.management.base import BaseCommand                                  # On importe le module Django BaseCommand
import http_request

from search.models import Aliment


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

                            new_row = Aliment(pnns_groups_1=category, product_name=name, nutriscore=nutriscore, url=url) # On insère les données dans la table Aliment, puis on sauvegarde les modifications après chaque insertion
                            new_row.save()
                        except:
                            pass
                
                print("Database successfully initialized")
