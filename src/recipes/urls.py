from django.urls import path
from .views import welcome, home, RecipeListView, recipe_detail, search_results

app_name = 'recipes'

urlpatterns = [
    path('welcome/', welcome, name='welcome'),  # Welcome page URL
    path('home/', home, name='home'),  # Home page URL
    path('recipes/', RecipeListView.as_view(), name='recipes_list'),
    path('recipes/<int:recipe_id>/', recipe_detail, name='recipe_detail'),
    path('search/', search_results, name='search_results'),
]