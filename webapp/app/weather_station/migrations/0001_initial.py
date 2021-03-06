# Generated by Django 3.2.4 on 2021-06-26 16:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WeatherStation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_key', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='WeatherRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_date', models.DateTimeField(auto_now_add=True, verbose_name='momento de publicacao')),
                ('temperature', models.DecimalField(decimal_places=2, max_digits=6)),
                ('humidity', models.DecimalField(decimal_places=2, max_digits=6)),
                ('light', models.DecimalField(decimal_places=2, max_digits=6)),
                ('pressure', models.DecimalField(decimal_places=2, max_digits=6)),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weather_station.weatherstation')),
            ],
        ),
    ]
