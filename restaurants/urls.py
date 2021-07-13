from django.urls import path

from restaurants.views import RestaurantDetailView, RestaurantFoodsView

urlpatterns = [
    path("/<int:restaurant_id>/foods", RestaurantFoodsView.as_view()),
    path("/<int:restaurant_id>", RestaurantDetailView.as_view()),  

]