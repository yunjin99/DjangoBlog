from django.urls import path

from . import views

urlpatterns = [
    path('<int:pk>/', views.PostDetail.as_view()),
    path('', views.PostList.as_view()),
    # path('<int:pk>/', views.single_post_page),
    # path('', views.index),
    path('category/<str:slug>/', views.show_category_posts),
    path('tag/<str:slug>/', views.show_tag_posts),
    path('create_post/', views.PostCreate.as_view()),
    path('update_post/<int:pk>/', views.PostUpdate.as_view())
]