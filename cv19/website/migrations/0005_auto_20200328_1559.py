# Generated by Django 2.1.5 on 2020-03-28 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_auto_20200328_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='cases_per_million',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='country',
            name='dead_per_million',
            field=models.FloatField(default=0.0),
        ),
    ]
