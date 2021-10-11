from django.conf.urls import url

from . import views                                        # import views so we can use them in urls.

urlpatterns = [
    url(r'^compte/', views.account_page),
    url(r'^create/$', views.create_account),
    url(r'^myfavorites/', views.consult_favorites),
    url(r'^connect/$', views.connect_account),
    url(r'^disconnect/', views.disconnect_account),
    url(r'^add_product/$', views.add_product_to_favorites),
    url(r'^my_favorites/', views.consult_favorites),
]
