# Generated by Django 2.2.8 on 2020-01-21 14:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20200121_1013'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='slog',
            new_name='slug',
        ),
    ]
