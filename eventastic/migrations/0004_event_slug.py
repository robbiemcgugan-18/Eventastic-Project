# Generated by Django 2.2.17 on 2021-03-15 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventastic', '0003_auto_20210315_1531'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='slug',
            field=models.SlugField(default=None, unique=True),
        ),
    ]
