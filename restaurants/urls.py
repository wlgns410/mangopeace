from django.urls import path

from restaurants.views import PopularRestaurantView, RestaurantDetailView, WishListView, RestaurantFoodsView

urlpatterns = [
    path("/<int:restaurant_id>/foods", RestaurantFoodsView.as_view()),
    path("/<int:restaurant_id>", RestaurantDetailView.as_view()),  
    path("", PopularRestaurantView.as_view()),
    path("/<int:restaurant_id>/wishlist", WishListView.as_view()),
]