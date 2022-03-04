# Generated by Django 3.2.12 on 2022-02-25 14:52

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20220219_1704'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating_num', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.module')),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.student')),
            ],
        ),
    ]