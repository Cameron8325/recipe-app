from django.urls import path
from .views import home, RecipeListView, recipe_detail

app_name = 'recipes'

urlpatterns = [
    path('', home, name='home'),
    path('recipes/', RecipeListView.as_view(), name='recipes_list'),
    path('recipes/<int:recipe_id>/', recipe_detail, name='recipe_detail'),
]
