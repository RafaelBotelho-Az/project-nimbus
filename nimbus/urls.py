from django.urls import path
from nimbus import views

app_name = 'nimbus'

urlpatterns = [
    path('', views.index, name='index'),
]
