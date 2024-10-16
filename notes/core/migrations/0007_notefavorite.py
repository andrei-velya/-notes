# Generated by Django 5.1 on 2024-10-18 18:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_note_profile'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NoteFavorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('note', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='note_favorite', to='core.note')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile_favorites', to='user.profile')),
            ],
            options={
                'verbose_name': 'Цитата в избранном',
                'verbose_name_plural': 'Цитаты в избранном',
            },
        ),
    ]
