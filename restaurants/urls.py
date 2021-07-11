from django.urls import path

from restaurants.views import RestaurantFoodView

urlpatterns = [
    path("/<int:restaurant_id>/food", RestaurantFoodView.as_view()),
]