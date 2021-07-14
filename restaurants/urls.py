from django.urls       import path

from restaurants.views import SubCategoryListView

urlpatterns = [
     path("/banner-list", SubCategoryListView.as_view()),
]