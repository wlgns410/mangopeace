from django.urls import path

from restaurants.views import RestaurantFoodsView

urlpatterns = [
    path("/<int:restaurant_id>/foods", RestaurantFoodsView.as_view()),
]