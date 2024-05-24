from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from .models import Recipe
from .forms import SearchForm, RecipeForm
from django.db.models import Q
import io
import matplotlib.pyplot as plt
import pandas as pd
from django.http import HttpResponse
from django.template.loader import render_to_string
import base64


def welcome(request):
    return render(request, "recipes/welcome.html")


@login_required
def home(request):
    featured_recipes = Recipe.objects.order_by("?")[:3]
    return render(
        request, "recipes/recipes_home.html", {"featured_recipes": featured_recipes}
    )


class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = "recipes/recipes_list.html"
    context_object_name = "recipes"


@login_required
def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)

    recipes = list(Recipe.objects.all().order_by("id"))
    current_index = next(
        index for (index, d) in enumerate(recipes) if d.id == recipe_id
    )

    next_index = (current_index + 1) % len(recipes)
    prev_index = (current_index - 1) % len(recipes)

    next_recipe_id = recipes[next_index].id
    prev_recipe_id = recipes[prev_index].id

    context = {
        "recipe": recipe,
        "next_recipe_id": next_recipe_id,
        "prev_recipe_id": prev_recipe_id,
    }

    return render(request, "recipes/recipe_detail.html", context)


@login_required
def search_results(request):
    form = SearchForm(request.GET)

    if form.is_valid():
        query = form.cleaned_data.get("query")
        cooking_time = form.cleaned_data.get("cooking_time")
        difficulty = form.cleaned_data.get("difficulty")

        recipes = Recipe.objects.all()

        if query:
            recipes = recipes.filter(
                Q(name__icontains=query)
                | Q(description__icontains=query)
                | Q(ingredients__icontains=query)
            )

        if cooking_time:
            recipes = recipes.filter(cooking_time__lte=cooking_time)

        if difficulty:
            recipes = recipes.filter(difficulty__iexact=difficulty)
    else:
        recipes = Recipe.objects.none()

    # Convert queryset to list of dictionaries
    recipe_list = list(recipes.values())

    # Convert list of dictionaries to Pandas DataFrame
    df = pd.DataFrame(recipe_list)

    # Group recipes by difficulty and count the number of recipes in each difficulty level
    difficulty_counts = df["difficulty"].value_counts()

    # Plotting a pie chart
    plt.figure(figsize=(8, 6))
    plt.pie(
        difficulty_counts,
        labels=difficulty_counts.index,
        autopct="%1.1f%%",
        startangle=140,
    )
    plt.title("Distribution of Difficulty Levels")
    plt.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.tight_layout()  # Adjust layout to prevent labels from being cut off

    # Save the pie chart as a BytesIO object
    pie_chart_buffer = io.BytesIO()
    plt.savefig(pie_chart_buffer, format="png")
    pie_chart_buffer.seek(0)

    # Plotting a bar chart for most popular ingredients
    # Combine and split ingredients into individual items
    ingredients_combined = " ".join(df["ingredients"]).split()

    # Count occurrences of each ingredient
    ingredient_counts = pd.Series(ingredients_combined).value_counts()

    # Get the top 10 most common ingredients
    top_ingredients = ingredient_counts.head(10)

    # Plotting a bar chart
    plt.figure(figsize=(10, 6))
    top_ingredients.plot(kind="bar")
    plt.xlabel("Ingredient")
    plt.ylabel("Number of Recipes")
    plt.title("Top 10 Most Popular Ingredients")
    plt.xticks(rotation=45)
    plt.tight_layout()  # Adjust layout to prevent labels from being cut off

    # Save the bar chart as a BytesIO object
    bar_chart_buffer = io.BytesIO()
    plt.savefig(bar_chart_buffer, format="png")
    bar_chart_buffer.seek(0)

    # Render the template with charts as base64 strings
    context = {
        "search_results": recipes,
        "form": form,
        "pie_chart_base64": base64.b64encode(pie_chart_buffer.getvalue()).decode(),
        "bar_chart_base64": base64.b64encode(bar_chart_buffer.getvalue()).decode(),
    }
    html = render_to_string("recipes/search_results.html", context)

    return HttpResponse(html)


@login_required
def add_recipe(request):
    form = RecipeForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("recipes:recipes_list")

    return render(request, "recipes/add_recipe.html", {"form": form})


@login_required
def about(request):
    return render(request, "recipes/about.html")
