# Generated by Django 4.2.16 on 2025-01-16 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0010_alter_osoba_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('artist', models.CharField(max_length=100)),
                ('album', models.CharField(max_length=100)),
                ('release_date', models.DateField()),
                ('genre', models.CharField(max_length=100)),
            ],
        ),
    ]