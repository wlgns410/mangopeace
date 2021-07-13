from django.urls import path

from restaurants.views import PopularRestaurantView, RestaurantDetailView, RestaurantReviewView

urlpatterns = [
    path("", PopularRestaurantView.as_view()),
    path("/<int:restaurant_id>", RestaurantDetailView.as_view()),
    path("/<int:restaurant_id>/reviews", RestaurantReviewView.as_view()),
]