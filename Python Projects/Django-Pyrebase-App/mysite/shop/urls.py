from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="Shop"),
    path('signup/', views.signUp, name="SignUp"),
    path('login/', views.logIn, name="LogIn"),
    path('postsignup/', views.postsignUp, name="PostSignUp"),
    path('postsignin/', views.postsignIn, name="PostSignIn"),
    path('purchase/', views.purchase, name="Purchase")
]