# Generated by Django 2.2.17 on 2021-04-04 19:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventastic', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='name',
            new_name='eventName',
        ),
    ]