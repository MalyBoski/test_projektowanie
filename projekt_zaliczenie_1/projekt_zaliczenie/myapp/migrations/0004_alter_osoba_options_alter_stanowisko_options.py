# Generated by Django 4.2.16 on 2025-01-15 16:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_osoba_stanowisko_delete_person_delete_team_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='osoba',
            options={'verbose_name_plural': 'Osoby'},
        ),
        migrations.AlterModelOptions(
            name='stanowisko',
            options={'verbose_name_plural': 'Stanowiska'},
        ),
    ]
