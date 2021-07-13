from django.urls       import path

from restaurants.views import RestaurantDetailView

urlpatterns = [
    path("/<int:restaurant_id>", RestaurantDetailView.as_view()),
]