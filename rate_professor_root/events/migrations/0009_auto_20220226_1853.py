# Generated by Django 3.2.12 on 2022-02-26 18:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_rename_identifier_professor_professor_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rating',
            old_name='module',
            new_name='module_code',
        ),
        migrations.RenameField(
            model_name='rating',
            old_name='professor_identifier',
            new_name='professor_id',
        ),
        migrations.RenameField(
            model_name='rating',
            old_name='rating_num',
            new_name='rating',
        ),
        migrations.RemoveField(
            model_name='rating',
            name='student_id',
        ),
    ]
