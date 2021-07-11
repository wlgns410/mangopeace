from django.urls import path

from restaurants.views import HighListView

urlpatterns = [
    path("/<int:restaurant_id>/high_ratings", HighListView.as_view())
]
