# Generated by Django 3.2.12 on 2022-02-19 15:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=120, verbose_name='Module Code')),
                ('name', models.CharField(max_length=120, verbose_name='Module Name')),
                ('year', models.IntegerField()),
                ('semester', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(2)])),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30, verbose_name='Student Username')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Student Email')),
                ('password', models.CharField(max_length=120, verbose_name='Student Password')),
            ],
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=30, verbose_name='First Name of Professor')),
                ('lastname', models.CharField(max_length=30, verbose_name='Lastname of Professor')),
                ('modules', models.ManyToManyField(blank=True, to='events.Module')),
            ],
        ),
        migrations.AddField(
            model_name='module',
            name='students',
            field=models.ManyToManyField(blank=True, to='events.Student'),
        ),
    ]
