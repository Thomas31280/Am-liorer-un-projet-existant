from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import login, logout
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from search.models import Favorites, Aliment
from search import views as search_views
from django.contrib.auth.models import User


def account_page(request):

    current_user = request.user
    username = current_user.username
    data_dict = { 'username': username }

    return render(request, 'user/compte.html', locals())

def create_account(request):

    obj = str(request.GET)                                                       # On utilise la méthode GET sur l'objet request de classe WSGIRequest. Cette méthode de la classe WSGIRequest permet de récupérer un dictionnaire qui contient les arguments passés à l'URL
    username = request.GET.get('username')                                       # On récupère la requête dans le dictionnaire ainsi créé. Ici, c'est la valeur de la clé username qu'on récupère
    email = request.GET.get('email')

    if email and username:

        try:
            new_user = User(username=username, email=email)                      # On commence par insérer le nouvel utilisateur dans la table par défaut User de Django, puis on save l'instance dans la table
            new_user.save()
            template = loader.get_template('user/compte.html')
            return HttpResponse(template.render(request=request))

        except:
            print("User can't be saved in table, check the constraints on table's fields")
            return render(request, '500.html', status=500)

    else:
        print("The datas passed in url parameters doesn't exist")
        return render(request, '500.html', status=500)


def connect_account(request):

    obj = str(request.GET)
    username = request.GET.get('username')
    email = request.GET.get('email')

    user = User.objects.filter(username=username, email=email).first()           # On va ici chercher un utilisateur qui match avec les informations rentrées dans les inputfields et récupérées dans les paramètre de l'URL qui correspond à cette vue. On va utiliser filter pour chercher une correspondance dans la table, mais on va surtout utiliser la fonction .first() sur l'objet queryset ainsi retourné, car on veut avoir une instance précise et non une queryset. Cela se justifie par l'utilisation que l'on va avoir de notre variable user

    if user is not None:
        login(request, user)                                                     # ... et c'est pour celà que l'on souhaitait une instance et non une queryset, car la méthode login de Django s'utilise sur une instance. Une queryset passée en paramètre de cette méthode renverrait une erreur
        print("Vous êtes bien connecté !")
        return search_views.index(request)                                       # On retourne à la page d'accueil
    else:
        print("Impossible de vous connecter")
        return render(request, '500.html', status=500)

def disconnect_account(request):

    try:
        logout(request)
        print("Vous avez été déconnecté avec succès !")

    except:
        print("Un problème est survenu et vous n'avez pas pu vous déconnecter !")

    return search_views.index(request)                                           # On retourne à la page d'accueil

def add_product_to_favorites(request):

    obj = str(request.GET)
    product_url = request.GET.get('url')                                         # On récupère l'id du produit dans l'URL

    try:
        current_user = request.user                                                  # Django nous permet de récupérer dirrectement l'utilisateur connecté à la session en cours à travers l'objet request. On va donc pourvoir récupérer ainsi l'instance de l'utilisateur connecté en base de données, avec tous ses attributs !
        user_id = current_user.id                                                    # C'est l'attribut id de l'instance qui nous intéresse ici
        user = User.objects.get(id=user_id)

        user = User.objects.get(id=user_id)

        try:
            aliment = Aliment.objects.get(url=product_url)                       # On tente de récupérer l'aliment qui correspond à l'url
            new_favorite = Favorites(product_id=aliment, user_id=user)           # On insère le nouveau favoris dans la table favorites, puis on save l'instance dans la table. A savoir que dans le cas d'attributs ayant une cardinalité avec d'autres tables ( donc sur lesquels il existe une foreign key ), l'ORM de Django exige qu'on lui passe un objet de type queryset pour remplir le champ de l'attribut !!!
            new_favorite.save()
            print("Aliment enregistré avec succès !")
            return search_views.index(request)
        
        except:
            print("L'aliment se trouve déjà dans vos favoris")
            return render(request, '500.html', status=500)

    except:
        print("Vous n'êtes pas connecté !")
        return render(request, '500.html', status=500)


def consult_favorites(request):

    current_user = request.user
    user_id = current_user.id

    if user_id:

        favorites = list(Favorites.objects.filter(user_id=user_id).values())         # On récupère tous les produits associé au compte de l'utilisateur en cours

        data = []                                                                    # On initialise une liste vide qui va contenir les produits qui correspondent aux id ainsi récupérés

        for product in favorites:
            data.append(Aliment.objects.get(id=product["product_id_id"]))

        print(data)

        # On découpe la liste des aliments sur plusieurs pages ( liste, nombre d'éléments pas page)
        paginator = Paginator(data, 6)
        # On récupère le numéro de la page actuelle
        page = request.GET.get('page')
        # On retourne uniquement les éléments qui concernent cette page
        try:
            my_favorites = paginator.get_page(page)
        except PageNotAnInteger:
            # Si le paramètre page n'est pas un int, on affiche la première page
            my_favorites = paginator.get_page(1)
        except EmptyPage:
            # Si la page est out of range, on affiche la dernière page de résultats
            my_favorites = paginator.get_page(paginator.num_pages)

        data_dict = { 'favorites': my_favorites, 'paginate': True }                  # On a ajouté une clé paginate dont la valeur est un booléen afin de se servir de ce booléen pour mettre l'affichage des boutons previous et next dans une structure conditionnelle au niveau du template

        return render(request, 'user/favorites.html', locals())                      # ... Et on s'en sert dans les templates !

    else:
        print("Vous n'êtes pas connecté !")
        return render(request, '500.html', status=500)
