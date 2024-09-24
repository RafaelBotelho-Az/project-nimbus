from django.urls import path
from nimbus import views

app_name = 'nimbus'

urlpatterns = [
    path('', views.index, name='index'),

    # posts
    path('post/<int:post_id>/', views.post, name='post'),
    path('post/create', views.createPost, name='create'),



    # path('post/<int:post_id>/update', views.post, name='post'),
    # path('post/<int:post_id>/delete', views.post, name='post'),

]
