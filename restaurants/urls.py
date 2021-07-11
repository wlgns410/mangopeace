from django.urls import path

from restaurants.views import RestaurantReviewView

urlpatterns = [
    path("/<int:restaurant_id>/review", RestaurantReviewView.as_view()),
]