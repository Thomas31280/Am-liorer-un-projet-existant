from django.conf.urls import url

from . import views                                        # import views so we can use them in urls.

urlpatterns = [
    url(r'^$', views.index, name = "index"),               # "/" will call the method "index" in "search.views.py"
    url(r'^result/$', views.search_substitute, name="result"),
    url(r'^aliment/$', views.info_aliment, name = "aliment"),
]
