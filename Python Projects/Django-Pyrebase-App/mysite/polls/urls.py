from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="Polls"),
    path("shop", views.shop, name="Poll-Shop"),
    
]