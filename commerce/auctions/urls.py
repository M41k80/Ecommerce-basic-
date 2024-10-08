from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    path('create', views.create_listing, name='create'),
    path('filter_category', views.filter_category, name='filter_category'),
    path('listing_product/<int:id>', views.listing_product, name='listing_product'),
    path('remove_watchlist/<int:id>', views.remove_watchlist, name='remove_watchlist'),
    path('add_watchlist/<int:id>', views.add_watchlist, name='add_watchlist'),
    path('display_watchlist', views.display_watchlist, name='display_watchlist'),
    path('add_comment/<int:id>', views.add_comment, name='add_comment'),
    path('add_bid/<int:id>', views.add_bid, name='add_bid'),
    path('close_auction/<int:id>', views.close_auction, name='close_auction'),




]
