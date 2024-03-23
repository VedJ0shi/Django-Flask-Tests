# Generated by Django 5.0.2 on 2024-03-23 00:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test1', '0002_alter_familymember_partner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='familymember',
            name='father',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fchildren', to='test1.familymember'),
        ),
        migrations.AlterField(
            model_name='familymember',
            name='mother',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mchildren', to='test1.familymember'),
        ),
    ]