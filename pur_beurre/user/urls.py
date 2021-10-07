from django.conf.urls import url

from . import views                                        # import views so we can use them in urls.

urlpatterns = [
    url(r'^compte/', views.account_page),
    url(r'^connect/$', views.create_account),
    url(r'^myfavorites/', views.consult_favorites),
]
