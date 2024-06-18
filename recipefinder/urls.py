from django.contrib import admin
from django.urls import path, include
from recipes import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('recipes.urls')),  # ルートパスをrecipesにマッピング
    path('accounts/', include('django.contrib.auth.urls')),
    path('fridge/', views.home, name='home'),
    path('delete_ingredient/', views.delete_ingredient, name='delete_ingredient'),
    path('search_recipes/', views.search_recipes, name='search_recipes'),
]
