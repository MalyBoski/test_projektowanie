# Generated by Django 4.2.16 on 2025-01-15 16:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_osoba_miesiac'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='osoba',
            options={'ordering': ['nazwisko'], 'verbose_name_plural': 'Osoby'},
        ),
    ]