from django.urls import path

from restaurants.views import RestaurantReviewView, RestaurantDetailView

urlpatterns = [
    path("/<int:restaurant_id>/review", RestaurantReviewView.as_view()),
    path("/<int:restaurant_id>", RestaurantDetailView.as_view()),
]