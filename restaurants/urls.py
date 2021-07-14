from django.urls import path

from restaurants.views import PopularRestaurantView, RestaurantView, RestaurantDetailView, WishListView

urlpatterns = [
    path("", RestaurantView.as_view()),
    path("/<int:restaurant_id>", RestaurantDetailView.as_view()),  
    path("/<int:restaurant_id>/wishlist", WishListView.as_view()),
    path("/popular", PopularRestaurantView.as_view())
]