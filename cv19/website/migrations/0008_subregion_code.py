# Generated by Django 2.1.5 on 2020-04-10 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_auto_20200330_2158'),
    ]

    operations = [
        migrations.AddField(
            model_name='subregion',
            name='code',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
