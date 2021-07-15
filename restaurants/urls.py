from django.urls import path

from restaurants.views import (
    PopularRestaurantView,
    RestaurantDetailView,
    WishListView,
    SubCategoryListView,
    RestaurantFoodsView,
    RestaurantReviewView,
    ReviewView,
    RestaurantView,
    FilteringView
)

urlpatterns = [
    path("/<int:restaurant_id>/foods", RestaurantFoodsView.as_view()),
    path("/<int:restaurant_id>", RestaurantDetailView.as_view()),  
    path("/banner-list", SubCategoryListView.as_view()),
    path("/<int:restaurant_id>/wishlist", WishListView.as_view()),
    path("/<int:restaurant_id>/review/<int:review_id>", ReviewView.as_view()),  
    path("/<int:restaurant_id>/reviews", RestaurantReviewView.as_view()),
    path("", RestaurantView.as_view()),
    path("/popular", PopularRestaurantView.as_view()),
    path("/search", FilteringView.as_view()),
]