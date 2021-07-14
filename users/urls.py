from django.urls import path

from users.views import SignInView, SignupView, UserDetailView

urlpatterns = [
    path("/signin", SignInView.as_view()),
    path("/signup", SignupView.as_view()),
    path("/detail", UserDetailView.as_view()),
]