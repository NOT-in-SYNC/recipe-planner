from django.contrib import admin
from django.urls import path
# Import the new views
from planner.views import home, add_recipe, browse_templates, copy_template

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('add/', add_recipe, name='add_recipe'),
    
    # New Paths
    path('templates/', browse_templates, name='browse_templates'),
    path('templates/copy/<int:template_id>/', copy_template, name='copy_template'),
]