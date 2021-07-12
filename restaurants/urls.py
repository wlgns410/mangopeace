from django.urls       import path

from restaurants.views import WishListView

urlpatterns = [
    path("/<int:restaurant_id>/wishlist", WishListView.as_view()),
]