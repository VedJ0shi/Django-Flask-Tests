# Generated by Django 5.0.2 on 2024-03-23 00:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Family',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='FamilyMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='first name')),
                ('age', models.PositiveSmallIntegerField(verbose_name='age (yrs)')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=32)),
                ('family', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='test1.family')),
                ('father', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='f_children', to='test1.familymember')),
                ('mother', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='m_children', to='test1.familymember')),
                ('partner', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='test1.familymember')),
                ('siblings', models.ManyToManyField(blank=True, to='test1.familymember')),
            ],
        ),
    ]