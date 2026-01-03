from django.urls import path
from . import views

urlpatterns = [
    path('', views.meal_plan_list, name='meal_plan_list'),
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
]