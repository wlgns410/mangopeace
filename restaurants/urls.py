from django.urls import path

from restaurants.views import PopularRestaurantView, RestaurantDetailView, WishListView, ReviewView

urlpatterns = [
    path("", PopularRestaurantView.as_view()),
    path("/<int:restaurant_id>", RestaurantDetailView.as_view()),  
    path("/<int:restaurant_id>/wishlist", WishListView.as_view()),
    path("/<int:restaurant_id>/review/<int:review_id>", ReviewView.as_view()),  
]