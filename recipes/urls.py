from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'recipes', views.RecipeViewSet)
router.register(r'ingredients', views.IngredientViewSet)
router.register(r'user-ingredients', views.UserIngredientViewSet)
router.register(r'recipe-ingredients', views.RecipeIngredientViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('fridge/', views.home, name='fridge'),
    path('delete_ingredient/', views.delete_ingredient, name='delete_ingredient'),
    path('search_recipes/', views.search_recipes, name='search_recipes'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),  # ここにPOSTメソッドを使ったログアウトを追加
    path('accounts/', include('django.contrib.auth.urls')),  # 標準のauth URLをインクルード
    path('get_and_save_recipes/<str:category_id>/', views.get_and_save_recipes, name='get_and_save_recipes'),
    path('add_ingredient/', views.add_ingredient, name='add_ingredient'),
    path('search_ingredients/', views.search_ingredients, name='search_ingredients'),
    path('search_results/', views.search_results, name='search_results'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),  # 新しいURLパターンを追加
]
