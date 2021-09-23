from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from search.models import Aliment
from search.models import Category

def index(request):
    template = loader.get_template('search/index.html')
    return HttpResponse(template.render(request=request))

def result(request):
    template = loader.get_template('search/result.html')
    return HttpResponse(template.render(request=request))

def aliment(request):
    template = loader.get_template('search/aliment.html')
    return HttpResponse(template.render(request=request))

def compte(request):
    template = loader.get_template('search/compte.html')
    return HttpResponse(template.render(request=request))

def info_aliment(request):

    obj = str(request.GET)                                                       # On utilise la méthode GET sur l'objet request de classe WSGIRequest. Cette méthode de la classe WSGIRequest permet de récupérer un dictionnaire qui contient les arguments passés à l'URL
    query = request.GET['query']                                                 # On récupère la requête dans le dictionnaire ainsi créé. Ici, on attends de la requête qu'elle soit l'URL d'un produit contenu dans la table search_aliment de la DB pur_beurre            

    result = list(Aliment.objects.filter(url=query).values())                    # Ici, on va récupérer l'instance de la base de donnée dont l'URL correspond à celle passée en paramètre. Par défaut, c'est un objet Django QuerySet qui est retourné. On va donc demander à ce que les attributs de cet objet soient retournées ( methode .values() ), puis on demande ensuite à ce que l'objet QuerySet soit converti en liste ( list(QuerySet_obj) )

    nutriscore = result[0]["nutriscore"]                                         # On attribue les données de cette liste qui nous intéressent à des variables
    cat_id = result[0]["pnns_groups_1_id"]
    category = list(Category.objects.filter(id=cat_id).values())[0]["category"]  # On récupère le nom de la catégorie dans la table category en utilisant la clé étrangère de la colonne pnns_group_1
    link_OFF = result[0]["url"]

    message = [nutriscore, " ", category, " ", link_OFF]

    return HttpResponse(message)                                                 # ... Et on s'en sert dans les templates !

def search_substitute(request):

    obj = str(request.GET)
    query = request.GET['query']

    prod_to_replace = list(Aliment.objects.filter(product_name=query).values())  # Comme dans la vue info_aliment, on a ciblé un produit avec des des filtres dans la base de données
    category = prod_to_replace[0]["pnns_groups_1_id"]
    nutriscore = prod_to_replace[0]["nutriscore"]

    substitutes = list(Aliment.objects.filter(pnns_groups_1=category).values())  # On réduit la liste des substitus possibles aux produits de la même catégorie que celui que l'utilisateur cherche à remplacer

    final_sort = []                                                              # On initialise une liste vide qui va contenir les produits qui sont substituables. On va remplir cette liste dans la boucle qui vient juste en dessous

    for product in substitutes:
        if nutriscore != "a":
            if product["nutriscore"] < nutriscore:
                final_sort.append(product)

        else:
            if product["nutriscore"] == "a":
                final_sort.append(product)

    message = final_sort

    return HttpResponse(message)                                                 # ... Et on s'en sert dans les templates !
