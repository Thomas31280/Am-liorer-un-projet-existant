from django.conf.urls import url

from . import views                                        # import views so we can use them in urls.

urlpatterns = [
    url(r'^compte/', views.account_page, name="compte"),
    url(r'^create/', views.create_account, name="create"),
    url(r'^connect/', views.connect_account, name="connect"),
    url(r'^disconnect/', views.disconnect_account, name="disconnect"),
    url(r'^add_product/$', views.add_product_to_favorites, name="add_product"),
    url(r'^my_favorites/', views.consult_favorites, name="my_favorites"),
    url(r'^update_profile_interface/', views.update_profile_interface, name="update_profile_interface"),
    url(r'^update/', views.update_profile, name="update_profile"),
]
