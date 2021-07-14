from django.urls import path

from restaurants.views import (
    PopularRestaurantView,
    RestaurantDetailView,
    WishListView,
    SubCategoryListView,
    RestaurantFoodsView,
    RestaurantReviewView
)

urlpatterns = [
    path("/<int:restaurant_id>/foods", RestaurantFoodsView.as_view()),
    path("/<int:restaurant_id>", RestaurantDetailView.as_view()),  
    path("", PopularRestaurantView.as_view()),
    path("/<int:restaurant_id>/wishlist", WishListView.as_view()),
    path("/banner-list", SubCategoryListView.as_view()),
    path("/<int:restaurant_id>/reviews", RestaurantReviewView.as_view()),

]