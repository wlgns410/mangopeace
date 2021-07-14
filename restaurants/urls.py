from django.urls import path

<<<<<<< HEAD
from restaurants.views import PopularRestaurantView, RestaurantDetailView, WishListView, ReviewView
=======
from restaurants.views import (
    PopularRestaurantView,
    RestaurantDetailView,
    WishListView,
    SubCategoryListView,
    RestaurantFoodsView,
    RestaurantReviewView,
    ReviewView
)
>>>>>>> main

urlpatterns = [
    path("", PopularRestaurantView.as_view()),
    path("/<int:restaurant_id>/foods", RestaurantFoodsView.as_view()),
    path("/<int:restaurant_id>", RestaurantDetailView.as_view()),  
    path("/banner-list", SubCategoryListView.as_view()),
    path("/<int:restaurant_id>/wishlist", WishListView.as_view()),
    path("/<int:restaurant_id>/review/<int:review_id>", ReviewView.as_view()),  
<<<<<<< HEAD
=======
    path("/<int:restaurant_id>/reviews", RestaurantReviewView.as_view()),
>>>>>>> main
]