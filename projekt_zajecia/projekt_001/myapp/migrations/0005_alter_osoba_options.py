# Generated by Django 5.1.4 on 2024-12-10 09:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_rename_name_team_imie_rename_country_team_panstwo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='osoba',
            options={'verbose_name': 'Osoba', 'verbose_name_plural': 'Ososby'},
        ),
    ]