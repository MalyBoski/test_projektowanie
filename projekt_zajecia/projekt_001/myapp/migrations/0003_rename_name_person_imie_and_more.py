# Generated by Django 5.1.3 on 2024-11-26 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_team_person'),
    ]

    operations = [
        migrations.RenameField(
            model_name='person',
            old_name='name',
            new_name='imie',
        ),
        migrations.RenameField(
            model_name='person',
            old_name='month_added',
            new_name='miesiac_dodany',
        ),
        migrations.RenameField(
            model_name='person',
            old_name='shirt_size',
            new_name='rozmiar_koszulki',
        ),
        migrations.AddField(
            model_name='osoba',
            name='miesiac_dodany',
            field=models.IntegerField(choices=[(1, 'Styczeń'), (2, 'Luty'), (3, 'Marzec'), (4, 'Kwiecień'), (5, 'Maj'), (6, 'Czerwiec'), (7, 'Lipiec'), (8, 'Sierpień'), (9, 'Wrzesień'), (10, 'Październik'), (11, 'Listopad'), (12, 'Grudzień')], default=1),
        ),
        migrations.AddField(
            model_name='osoba',
            name='rozmiar_koszulki',
            field=models.CharField(choices=[('S', 'Small'), ('M', 'Medium'), ('L', 'Large')], default='S', max_length=1),
        ),
    ]
