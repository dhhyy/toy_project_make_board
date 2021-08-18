from django.urls import path
from .views      import SignUpView, SignInView, Example

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/signin', SignInView.as_view()),
    path('/decorator-test', Example.as_view())
]