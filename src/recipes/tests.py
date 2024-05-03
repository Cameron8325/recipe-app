from django.test import TestCase
from .models import Recipe

class RecipeModelTest(TestCase):
    def setUp(self):
        self.recipe = Recipe.objects.create(
            name='Test Recipe',
            ingredients='Ingredient 1, Ingredient 2',
            cooking_time=30,
            difficulty='Easy'
        )

    def test_recipe_creation(self):
        """Test the creation of a recipe"""
        self.assertEqual(self.recipe.name, 'Test Recipe')
        self.assertEqual(self.recipe.ingredients, 'Ingredient 1, Ingredient 2')
        self.assertEqual(self.recipe.cooking_time, 30)
        self.assertEqual(self.recipe.difficulty, 'Easy')

    def test_recipe_update(self):
        """Test updating a recipe"""
        self.recipe.name = 'Updated Recipe'
        self.recipe.save()
        updated_recipe = Recipe.objects.get(id=self.recipe.id)
        self.assertEqual(updated_recipe.name, 'Updated Recipe')

    def test_recipe_deletion(self):
        """Test deleting a recipe"""
        recipe_id = self.recipe.id
        self.recipe.delete()
        with self.assertRaises(Recipe.DoesNotExist):
            Recipe.objects.get(id=recipe_id)
