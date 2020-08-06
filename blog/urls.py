from django.urls import path
from . import views

urlpatterns = [
    # localhost:8000/ 으로 요청오면 views.post_list를 보여준다.
    path('', views.post_list, name='post_list'),
    # localhost:8000/post/5
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    # localhost:8000/post/new/
    path('post/new/', views.post_new, name='post_new'),
    # localhost:8000/post/5/edit/
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    # localhost:8000/post/5/remove
    path('post/<int:pk>/remove/', views.post_remove, name='post_remove'),
]