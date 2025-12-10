from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='app3_index'),
    path("users/", views.user_list, name="mcat_user_list"),

]
