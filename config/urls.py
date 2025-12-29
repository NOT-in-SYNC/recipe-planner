from django.contrib import admin
from django.urls import path
from planner.views import home, add_recipe  # <-- Import add_recipe

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('add/', add_recipe, name='add_recipe'), # <-- Add this line
]