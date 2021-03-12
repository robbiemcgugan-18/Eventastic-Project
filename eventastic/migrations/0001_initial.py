# Generated by Django 2.2.17 on 2021-03-12 14:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoryName', models.CharField(max_length=30, unique=True)),
                ('categoryPicture', models.ImageField(upload_to='')),
                ('categoryDescription', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DOB', models.DateField()),
                ('profilePicture', models.ImageField(upload_to='')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eventName', models.CharField(max_length=30, unique=True)),
                ('eventDescription', models.CharField(max_length=200)),
                ('start', models.DateTimeField()),
                ('numberInterested', models.IntegerField()),
                ('eventPicture', models.ImageField(upload_to='')),
                ('address', models.CharField(max_length=40)),
                ('postcode', models.CharField(max_length=8)),
                ('averageRating', models.DecimalField(decimal_places=2, max_digits=3)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eventastic.Category')),
                ('createdBy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eventastic.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('posted', models.DateTimeField(auto_now_add=True)),
                ('comment', models.CharField(max_length=100)),
                ('eventName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eventastic.Event')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eventastic.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='Attend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(default=0)),
                ('eventName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eventastic.Event')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eventastic.UserProfile')),
            ],
        ),
    ]
