from django.urls import path
from . import views

urlpatterns = [
    path("add/", views.AddPost.as_view()),
    path("<int:pk>/", views.PostDetail.as_view()),
    path("", views.GetAllPosts.as_view()),
]
