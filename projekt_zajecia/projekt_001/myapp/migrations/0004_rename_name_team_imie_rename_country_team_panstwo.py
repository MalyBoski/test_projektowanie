# Generated by Django 5.1.3 on 2024-11-26 17:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_rename_name_person_imie_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='team',
            old_name='name',
            new_name='imie',
        ),
        migrations.RenameField(
            model_name='team',
            old_name='country',
            new_name='panstwo',
        ),
    ]