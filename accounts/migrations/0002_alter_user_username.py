# Generated by Django 5.0.4 on 2024-06-06 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(max_length=25, unique=True),
        ),
    ]
