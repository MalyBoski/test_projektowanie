# Generated by Django 5.1.4 on 2024-12-10 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_alter_osoba_options_alter_stanowisko_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='person',
            options={'verbose_name': 'Osobatest', 'verbose_name_plural': 'Osobytest'},
        ),
        migrations.AlterModelOptions(
            name='team',
            options={'verbose_name': 'Zespół', 'verbose_name_plural': 'Zespoły'},
        ),
        migrations.AddField(
            model_name='person',
            name='pseudonim',
            field=models.CharField(default='', max_length=100),
        ),
    ]