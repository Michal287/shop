"""shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from shop_apk.views import RegisterView, UserDetailView, ProductFrontListView, ProductAddView, ProductDeleteView, \
    ProductDetailView, ProductsListUserView, cart_add, cart_detail, cart_remove, ProductListView, add_or_remove_favourite, \
    FavouriteListView, OpinionUserListView, OpinionUserAddView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('rejestracja/', RegisterView.as_view(), name='register'),
    path('logowanie/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('wylogowanie/', auth_views.LogoutView.as_view(), name='logout'),
    path('logowanie/reset-hasla/start', auth_views.PasswordResetView.as_view(), name='password_reset_view'),#tworzenie formularza z mailem
    path('logowanie/reset-hasla/wysylanie-maila', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),#pomyślne wysłany mail
    path('logowanie/reset-hasla/nowe-haslo/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),#Weryfikacja i tworzenie formularza
    path('logowanie/reset-hasla/koniec', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),#Udało się zresetować hasło
    path('ustawienia/', UserDetailView.as_view(), name='user_detail'),
    path('produkt/twoje-produkty/', ProductsListUserView.as_view(), name='products_user'),
    path('', ProductFrontListView.as_view(), name='products_front_list'),
    path('kategoria/<category_slug>/', ProductListView.as_view(), name='products_list_by_category'),
    path('produkt/dodaj/', ProductAddView.as_view(), name='product_add'),
    path('produkt/usun/<int:id>/', ProductDeleteView.as_view(), name='product_delete'),
    path('produkt/<id>/<slug>', ProductDetailView.as_view(), name='product_detail'),
    path('produkt/ulubione/dodaj_usun/<id>/', add_or_remove_favourite, name='add_remove_favorite'),
    path('ulubione/', FavouriteListView.as_view(), name='favourite_list'),
    path('koszyk/dodaj/<id>/', cart_add, name='cart_add'),
    path('koszyk/usun/<id>/', cart_remove, name='cart_remove'),
    path('koszyk/', cart_detail, name='cart_detail'),
    path('opinie/<id>/', OpinionUserListView.as_view(), name='opinion_user_list'),
    path('opinie/<id>/dodaj/', OpinionUserAddView.as_view(), name='opinion_user_add'),


]
