from django import forms
from .models import Recipe

class SearchForm(forms.Form):
    query = forms.CharField(required=False, label='Search recipes')
    cooking_time = forms.IntegerField(required=False, label='Cooking time (minutes)')
    difficulty = forms.ChoiceField(required=False, label='Difficulty', choices=(
        ('', 'Select difficulty'),
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Intermediate', 'Intermediate'),
        ('Hard', 'Hard'),
    ))

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'ingredients', 'cooking_time', 'difficulty', 'pic']