# Generated by Django 2.1.5 on 2020-03-28 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_auto_20200328_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='first_case_date',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='subregion',
            name='first_case_date',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
