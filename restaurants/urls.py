from django.urls import path

from restaurants.views import (
    PopularView,
    RestaurantDetailView,
    WishListView,
    BannerView,
    RestaurantFoodsView,
    RestaurantReviewView,
    ReviewView,
    RestaurantView,
    FilteringView
)

urlpatterns = [
    path("/<int:restaurant_id>/foods", RestaurantFoodsView.as_view()),
    path("/<int:restaurant_id>", RestaurantDetailView.as_view()),  
    path("/banner", BannerView.as_view()),
    path("/<int:restaurant_id>/wishlist", WishListView.as_view()),
    path("/<int:restaurant_id>/review/<int:review_id>", ReviewView.as_view()),  
    path("/<int:restaurant_id>/reviews", RestaurantReviewView.as_view()),
    path("/restaurant-list/<int:restaurant_id>", RestaurantView.as_view()),
    path("/popular", PopularView.as_view()),
    path("/search", FilteringView.as_view()),
]