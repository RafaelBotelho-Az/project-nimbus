from django.urls import path
from nimbus import views

app_name = 'nimbus'

urlpatterns = [
    path('', views.index, name='index'),

    # posts
    path('post/<int:post_id>/', views.post, name='post'),
    path('post/create', views.createPost, name='create'),

    # user
    path('user/register', views.createUser, name='register'),
    path('user/login', views.loginView, name='login'),
    path('user/logout', views.logoutView, name='logout'),



]
