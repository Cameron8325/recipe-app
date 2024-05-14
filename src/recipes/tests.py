from django.test import TestCase
from django.urls import reverse
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

    def test_recipes_list_view(self):
        response = self.client.get(reverse('recipes:recipes_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.recipe.name)

    def test_recipe_detail_view(self):
        response = self.client.get(reverse('recipes:recipe_detail', args=[self.recipe.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.recipe.name)
        self.assertContains(response, self.recipe.description)
        self.assertContains(response, self.recipe.ingredients)
        self.assertContains(response, self.recipe.cooking_time)
        self.assertContains(response, self.recipe.difficulty)
