# admin.py

from django.contrib import admin
from .models import Ingredient, Recipe, UserIngredient, RecipeIngredient

admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(UserIngredient)
admin.site.register(RecipeIngredient)
