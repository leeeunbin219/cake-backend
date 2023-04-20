from django.urls import path
from . import views

urlpatterns = [
    path("", views.TableShowView.as_view()),
    path("new/", views.NewTable.as_view()),
    path("pick/", views.PickCakeView.as_view()),
    path("pick/<int:pk>/", views.LetterView.as_view()),
]