from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(required=False, label='Search recipes')
    cooking_time = forms.IntegerField(required=False, label='Cooking time (minutes)')
    difficulty = forms.ChoiceField(required=False, label='Difficulty', choices=(
        ('', 'Select difficulty'),
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ))
