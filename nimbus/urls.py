from django.urls import path
from nimbus import views

app_name = 'nimbus'

urlpatterns = [
    path('', views.index, name='index'),
    path('sobre/', views.sobre, name='sobre'),


    # posts
    path('post/<int:post_id>/', views.post, name='post'),
    path('post/create/', views.createPost, name='create'),
    path('post/<int:art_id>/like/', views.like_art, name='like_art'),

    # user
    path('user/register/', views.createUser, name='register'),
    path('user/login/', views.loginView, name='login'),
    path('user/logout/', views.logoutView, name='logout'),
    path('user/perfil/<username>/', views.perfil, name='perfil'),

]
