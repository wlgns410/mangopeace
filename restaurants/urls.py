from django.urls import path

from restaurants.views import PopularRestaurantView, RestaurantDetailView

urlpatterns = [
    path("/popular", PopularRestaurantView.as_view()),
    path("/<int:restaurant_id>", RestaurantDetailView.as_view()),  
]