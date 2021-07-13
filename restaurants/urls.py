from django.urls       import path

from restaurants.views import RestaurantDetailView, TopListView

urlpatterns = [
    path("/<int:restaurant_id>", RestaurantDetailView.as_view()),
    path("", TopListView.as_view()),
]