from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_listing", views.add_listing, name="add_listing"),
    path("listing/<str:title>", views.listing, name="listing"),
    path("listing/<str:title>/watchlist", views.add_watchlist, name="add_watchlist"),
    path("listing/<str:title>/delete_watchlist", views.delete_watchlist, name="delete_watchlist"),
    path("listing/<str:title>/place_bid", views.place_bid, name="place_bid"),
    path("listing/<str:title>/concretized", views.concretized, name="concretized"),
    path("listing/<str:title>/comment", views.comment, name="comment"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("item/<str:category>", views.category, name="category")
]
