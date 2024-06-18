from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

class Recipe(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    food_image_url = models.URLField(default='https://example.com/default.jpg')
    recipe_indication = models.CharField(max_length=255, default='')  # デフォルト値を設定
    recipe_cost = models.CharField(max_length=255, default='')
    materials = models.TextField(default='[]')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

class UserIngredient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
