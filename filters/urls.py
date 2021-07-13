from django.urls import path

from filters.views import FilteringVeiw

urlpatterns = [
    path('/search', FilteringVeiw.as_view()),
]