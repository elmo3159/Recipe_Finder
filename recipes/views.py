from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST, require_GET
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from recipes.serializers import UserSerializer, IngredientSerializer, RecipeSerializer, UserIngredientSerializer, RecipeIngredientSerializer
from recipes.models import Recipe, Ingredient, RecipeIngredient, UserIngredient
from recipes.hiragana_to_kanji import hiragana_to_kanji, convert_hiragana_to_kanji, convert_hiragana_to_katakana
from recipes.forms import CustomUserCreationForm, CustomUserChangeForm
import requests
import json

API_KEY = '1046289489798689204'
RECIPE_BASE_URL = 'https://app.rakuten.co.jp/services/api/Recipe/CategoryList/20170426'

def fetch_recipes(category_id):
    params = {
        'applicationId': API_KEY,
        'categoryId': category_id
    }
    try:
        response = requests.get(RECIPE_BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching recipes: {e}")
        return None

def save_recipe_data(recipes):
    for recipe in recipes:
        recipe_obj, created = Recipe.objects.get_or_create(
            title=recipe['recipeTitle'],
            url=recipe['recipeUrl']
        )
        for ingredient in recipe['recipeMaterial']:
            ingredient_obj, created = Ingredient.objects.get_or_create(name=ingredient)
            RecipeIngredient.objects.get_or_create(
                recipe=recipe_obj,
                ingredient=ingredient_obj
            )

def get_and_save_recipes(request, category_id):
    data = fetch_recipes(category_id)
    if data and 'result' in data:
        save_recipe_data(data['result'])
        return render(request, 'recipes/success.html')
    else:
        return render(request, 'recipes/error.html', {'message': 'Failed to fetch recipes'})

@login_required
def home(request):
    user_ingredients = UserIngredient.objects.filter(user=request.user).select_related('ingredient')
    return render(request, 'recipes/fridge.html', {'user_ingredients': user_ingredients})

@require_POST
@login_required
def add_ingredient(request):
    data = json.loads(request.body)
    name = data.get('name')
    if name:
        if name in hiragana_to_kanji:
            name = hiragana_to_kanji[name]
        ingredient, created = Ingredient.objects.get_or_create(name=name)
        UserIngredient.objects.get_or_create(user=request.user, ingredient=ingredient)
        return JsonResponse({'success': True, 'ingredient': {'id': ingredient.id, 'name': ingredient.name}})
    return JsonResponse({'success': False})

@require_POST
@login_required
def delete_ingredient(request):
    data = json.loads(request.body)
    ids = data.get('ids')
    if ids:
        UserIngredient.objects.filter(user=request.user, ingredient_id__in=ids).delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@require_GET
def search_ingredients(request):
    query = request.GET.get('query', '')
    if query:
        kanji_query = convert_hiragana_to_kanji(query)
        katakana_query = convert_hiragana_to_katakana(query)
        ingredients = Ingredient.objects.filter(name__icontains=query) | \
                      Ingredient.objects.filter(name__icontains=kanji_query) | \
                      Ingredient.objects.filter(name__icontains=katakana_query)
        ingredients = ingredients.values('id', 'name')
        return JsonResponse(list(ingredients), safe=False)
    return JsonResponse([], safe=False)

@require_POST
@login_required
@require_POST
@login_required
def search_recipes(request):
    data = json.loads(request.body)
    ingredients = data.get('ingredients', [])
    if not ingredients:
        user_ingredients = UserIngredient.objects.filter(user=request.user).select_related('ingredient')
        ingredients = [ui.ingredient.name for ui in user_ingredients]
    if ingredients:
        user_ingredients = [convert_hiragana_to_kanji(ing) for ing in ingredients]
        condiments = ['塩', '砂糖', '醤油', '味噌', '酢', 'みりん', '酒', '胡椒', 'だし', '油', 'バター', '水', 'ごはん', '白米', 'お米']

        recipes = Recipe.objects.all()
        recipe_scores = []

        for recipe in recipes:
            recipe_materials = json.loads(recipe.materials)
            match_count = sum(1 for ing in user_ingredients if ing in recipe_materials)
            non_match_count = sum(1 for ing in recipe_materials if ing not in user_ingredients + condiments)
            score = match_count - non_match_count
            recipe_scores.append((score, recipe))

        sorted_recipes = sorted(recipe_scores, key=lambda x: x[0], reverse=True)
        recipes_data = [{'title': recipe.title, 'url': recipe.url, 'materials': json.loads(recipe.materials)} for _, recipe in sorted_recipes]

        return JsonResponse({'recipes': recipes_data})
    return JsonResponse({'recipes': []})

@login_required
def search_results(request):
    if request.method == 'POST':
        recipes = json.loads(request.POST.get('recipes', '[]'))
        request.session['recipes'] = recipes  # セッションに保存
    else:
        recipes = request.session.get('recipes', [])

    page = request.GET.get('page', 1)
    paginator = Paginator(recipes, 15)  # 1ページに15件のレシピを表示

    try:
        paginated_recipes = paginator.page(page)
    except PageNotAnInteger:
        paginated_recipes = paginator.page(1)
    except EmptyPage:
        paginated_recipes = paginator.page(paginator.num_pages)

    # 各レシピの詳細情報を含める
    for recipe in paginated_recipes:
        recipe_obj = Recipe.objects.get(title=recipe['title'])
        recipe['food_image_url'] = recipe_obj.food_image_url
        recipe['recipe_indication'] = recipe_obj.recipe_indication
        recipe['recipe_cost'] = recipe_obj.recipe_cost
        recipe['materials'] = recipe_obj.materials

    return render(request, 'recipes/search_results.html', {
        'recipes': paginated_recipes,
        'page_obj': paginated_recipes,
    })

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@require_POST
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, instance=request.user)
        password_form = PasswordChangeForm(user=request.user, data=request.POST)
        if user_form.is_valid() and password_form.is_valid():
            user_form.save()
            user = password_form.save()
            update_session_auth_hash(request, user)
            return redirect('home')
    else:
        user_form = CustomUserChangeForm(instance=request.user)
        password_form = PasswordChangeForm(user=request.user)
    return render(request, 'recipes/edit_profile.html', {
        'user_form': user_form,
        'password_form': password_form
    })

def category_view(request):
    ingredients = Ingredient.objects.all()
    recipes = Recipe.objects.all()
    return render(request, 'recipes/category_view.html', {'ingredients': ingredients, 'recipes': recipes})

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

class UserIngredientViewSet(viewsets.ModelViewSet):
    queryset = UserIngredient.objects.all()
    serializer_class = UserIngredientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class RecipeIngredientViewSet(viewsets.ModelViewSet):
    queryset = RecipeIngredient.objects.all()
    serializer_class = RecipeIngredientSerializer