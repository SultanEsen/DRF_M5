# Generated by Django 4.1.1 on 2022-09-29 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_app', '0006_alter_review_stars'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='stars',
            field=models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], null=True),
        ),
    ]