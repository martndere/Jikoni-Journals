from django.urls import path
from . import views

urlpatterns = [
    path('', views.map_view, name='map_view'),
    path('api/pins/', views.map_pins_api, name='map_pins_api'),
    path('pin/<int:pk>/recipes/', views.recipes_for_pin, name='pin_recipes'),
]