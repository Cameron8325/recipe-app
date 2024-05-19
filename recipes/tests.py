from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Recipe

class RecipeAppTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.recipe = Recipe.objects.create(
            name='Test Recipe',
            description='Test Description',
            ingredients='ingredient1, ingredient2',
            cooking_time=30,
            difficulty='Easy'
        )
    
    def test_home_page(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipes_home.html')

    def test_recipe_list_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('recipes:recipes_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipes_list.html')
        self.assertContains(response, self.recipe.name)

    def test_recipe_detail_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('recipes:recipe_detail', args=[self.recipe.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe_detail.html')
        self.assertContains(response, self.recipe.name)
        self.assertContains(response, self.recipe.description)

    def test_search_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('recipes:search_results'), {
            'query': 'Test',
            'cooking_time': 30,
            'difficulty': 'Easy'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/search_results.html')
        self.assertContains(response, self.recipe.name)
        self.assertContains(response, self.recipe.description)

    def test_add_recipe_view_get(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('recipes:add_recipe'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/add_recipe.html')

    def test_add_recipe_view_post(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('recipes:add_recipe'), {
            'name': 'New Recipe',
            'description': 'New Description',
            'ingredients': 'ingredient1, ingredient2',
            'cooking_time': 40,
            'difficulty': 'Medium',
            'pic': 'no_picture.jpg'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Recipe.objects.filter(name='New Recipe').exists())

    def test_protected_views_redirect(self):
        response = self.client.get(reverse('recipes:recipes_list'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('recipes:recipes_list')}")

        response = self.client.get(reverse('recipes:recipe_detail', args=[self.recipe.id]))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('recipes:recipe_detail', args=[self.recipe.id])}")

    def test_welcome_view(self):
        response = self.client.get(reverse('recipes:welcome'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/welcome.html')

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/login.html')

        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertRedirects(response, reverse('recipes:home'))

    def test_logout_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/success.html')
