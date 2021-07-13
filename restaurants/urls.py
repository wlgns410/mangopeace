from django.urls import path

from restaurants.views import PopularRestaurantView

urlpatterns = [
    path("/popular", PopularRestaurantView.as_view())
]