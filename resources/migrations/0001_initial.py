# Generated by Django 2.2.10 on 2022-11-16 18:08

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
                ('name', models.CharField(max_length=1250)),
            ],
        ),
        migrations.CreateModel(
            name='Resources',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1250)),
                ('description', models.CharField(max_length=225)),
                ('duration', models.CharField(max_length=225)),
                ('link', models.CharField(max_length=225)),
                ('resource_file', models.FileField(default=None, max_length=250, null=True, upload_to='resources/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(default=0, null=True)),
                ('total_time_spend', models.IntegerField(default=0)),
                ('resources', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resources.Resources')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TimeSpendUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_user', models.DateTimeField()),
                ('time_spend_by_user', models.IntegerField(default=0)),
                ('status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='resources.Status')),
            ],
        ),
        migrations.AddField(
            model_name='resources',
            name='User',
            field=models.ManyToManyField(null=True, through='resources.Status', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='resources',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='resources.Category'),
        ),
    ]
