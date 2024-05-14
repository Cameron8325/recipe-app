from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Recipe

def home(request):
    featured_recipes = Recipe.objects.order_by('?')[:3]
    return render(request, 'recipes/recipes_home.html', {'featured_recipes': featured_recipes})

class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/recipes_list.html'
    context_object_name = 'recipes'

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})
