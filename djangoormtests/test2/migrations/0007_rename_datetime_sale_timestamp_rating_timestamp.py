# Generated by Django 5.0.2 on 2024-05-20 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test2', '0006_alter_rating_stars'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sale',
            old_name='datetime',
            new_name='timestamp',
        ),
        migrations.AddField(
            model_name='rating',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
