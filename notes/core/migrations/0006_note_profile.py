# Generated by Django 5.1 on 2024-10-18 17:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_feedback_alter_note_category'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='profile',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='profile_notes', to='user.profile'),
            preserve_default=False,
        ),
    ]
