# Generated by Django 5.1 on 2024-08-31 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='author',
            field=models.CharField(default='Автор неизвестен', max_length=255),
        ),
    ]
