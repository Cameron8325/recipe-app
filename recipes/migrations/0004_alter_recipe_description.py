# Generated by Django 5.0.4 on 2024-05-24 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0003_recipe_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipe",
            name="description",
            field=models.CharField(default="No description available.", max_length=255),
        ),
    ]
