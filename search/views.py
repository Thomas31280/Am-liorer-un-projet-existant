from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import logging

from search.models import Aliment, Category

# Get an instance of a logger
logger = logging.getLogger(__name__)

def index(request):
    template = loader.get_template('search/index.html')
    return HttpResponse(template.render(request=request))


def info_aliment(request):

    obj = str(request.GET)                                                       # On utilise la méthode GET sur l'objet request de classe WSGIRequest. Cette méthode de la classe WSGIRequest permet de récupérer un dictionnaire qui contient les arguments passés à l'URL
    query = request.GET.get('query')                                             # On récupère la requête dans le dictionnaire ainsi créé. Ici, on attends de la requête qu'elle soit l'URL d'un produit contenu dans la table search_aliment de la DB pur_beurre

    result = list(Aliment.objects.filter(url=query).values())                    # Ici, on va récupérer l'instance de la base de donnée dont l'URL correspond à celle passée en paramètre. Par défaut, c'est un objet Django QuerySet qui est retourné. On va donc demander à ce que les attributs de cet objet soient retournées ( methode .values() ), puis on demande ensuite à ce que l'objet QuerySet soit converti en liste ( list(QuerySet_obj) )

    nutriscore = result[0]["nutriscore"]                                         # On attribue les données de cette liste qui nous intéressent à des variables
    cat_id = result[0]["pnns_groups_1_id"]
    category = list(Category.objects.filter(id=cat_id).values())[0]["category"]  # On récupère le nom de la catégorie dans la table category en utilisant la clé étrangère de la colonne pnns_group_1
    link_OFF = result[0]["url"]
    product_name = result[0]["product_name"]

    data_dict = {"nutri": nutriscore, "cat": category, "url": link_OFF,
                 "name": product_name}
    template = loader.get_template('search/aliment.html')

    return render(request, 'search/aliment.html', locals())                      # ... Et on s'en sert dans les templates !


def search_substitute(request):

    obj = str(request.GET)
    query = request.GET.get('query')
    
    logger.info('New search', exc_info=True, extra={
        # Optionally pass a request and we'll grab any information we can
        'request': request,
    })
    
    if query:

        try:

            prod_to_replace = list(Aliment.objects.filter(product_name=query).values())  # Comme dans la vue info_aliment, on a ciblé un produit avec des des filtres dans la base de données
            product_name = query                                                         # On va se servir de cette variable dans le template
            category = prod_to_replace[0]["pnns_groups_1_id"]
            nutriscore = prod_to_replace[0]["nutriscore"]
            substitutes = Aliment.objects.filter(pnns_groups_1=category)                 # On réduit la liste des substitus possibles aux produits de la même catégorie que celui que l'utilisateur cherche à remplacer

            final_sort = []                                                              # On initialise une liste vide qui va contenir les produits qui sont substituables. On va remplir cette liste dans la boucle qui vient juste en dessous

            for product in substitutes:
                if nutriscore != "a":
                    if product.nutriscore < nutriscore:
                        final_sort.append(product)

                else:
                    if product.nutriscore == "a":
                        final_sort.append(product)

            data = final_sort

            # On découpe la liste des aliments sur plusieurs pages ( liste, nombre d'éléments pas page)
            paginator = Paginator(data, 6)
            # On récupère le numéro de la page actuelle
            page = request.GET.get('page')
            # On retourne uniquement les éléments qui concernent cette page
            try:
                aliments = paginator.get_page(page)
            except PageNotAnInteger:
                # Si le paramètre page n'est pas un int, on affiche la première page
                aliments = paginator.get_page(1)
            except EmptyPage:
                # Si la page est out of range, on affiche la dernière page de résultats
                aliments = paginator.get_page(paginator.num_pages)

            data_dict = {'aliments': aliments, 'paginate': True}                         # On a ajouté une clé paginate dont la valeur est un booléen afin de se servir de ce booléen pour mettre l'affichage des boutons previous et next dans une structure conditionnelle au niveau du template

            return render(request, 'search/result.html', locals())                       # ... Et on s'en sert dans les templates !

        except IndexError:                                                               # Une erreur d'index signifie que prod_to_replace n'a pas la structure attendue, et donc que le produit n'existe pas en base de données
            print("Le produit recherché ne se trouve pas en base de données")
            return render(request, '500.html', status=500)

    else:
        print("Vous avez envoyé un champ de recherche vide")
        return render(request, '500.html', status=500)
