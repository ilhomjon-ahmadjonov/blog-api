from django.urls import path
from .views import (PostListCreateView,PostDetailView,PostLikeView,CommentListCreateView,CommentDetailView,)


urlpatterns = [
    path('posts/', PostListCreateView.as_view()),
    path('posts/<int:pk>/', PostDetailView.as_view()),
    path('posts/<int:pk>/like/', PostLikeView.as_view()),

    path('posts/<int:post_pk>/comments/', CommentListCreateView.as_view()),
    path('posts/<int:post_pk>/comments/<int:pk>/', CommentDetailView.as_view()),
]