from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('main', views.main),
    path('add_plant', views.add_plant),
    path('update_plant/<int:plant_id>', views.update_plant),
    path('delete/<plant_id>', views.destroy_plant),
    path('plant/<int:plant_id>', views.plant_profile),
    path('logout', views.logout),

]
