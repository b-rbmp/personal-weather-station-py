# Generated by Django 3.2.4 on 2021-06-27 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather_station', '0002_alter_weatherrecord_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weatherrecord',
            name='record_date',
            field=models.DateTimeField(verbose_name='momento de publicacao'),
        ),
    ]
