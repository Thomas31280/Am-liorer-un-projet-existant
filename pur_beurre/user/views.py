from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from search.models import Favorites
from django.contrib.auth.models import User


def account_page(request):
    template = loader.get_template('user/compte.html')
    return HttpResponse(template.render(request=request))

def create_account(request):

    obj = str(request.GET)                                                       # On utilise la méthode GET sur l'objet request de classe WSGIRequest. Cette méthode de la classe WSGIRequest permet de récupérer un dictionnaire qui contient les arguments passés à l'URL
    username = request.GET.get('username')                                       # On récupère la requête dans le dictionnaire ainsi créé. Ici, c'est la valeur de la clé username qu'on récupère
    email = request.GET.get('email')

    print("The username is : ", username, " and the mail is : ", email)

    if email and username:

        try:
            new_user = User(username=username, email=email)                  # On commence par insérer le nouvel utilisateur dans la table par défaut User de Django, puis on save l'instance dans la table
            new_user.save()
        except:
            print("User can't be saved in table, check the constraints on table's fields")

    else:
        print("The datas passed in url parameters aren't valids")

    template = loader.get_template('user/compte.html')
    return HttpResponse(template.render(request=request))

def connect_account(request):
    pass

def disconnect_account(request):
    pass

def add_product_to_favorites(request):
    pass

def consult_favorites(request):
    template = loader.get_template('user/favorites.html')
    return HttpResponse(template.render(request=request))
