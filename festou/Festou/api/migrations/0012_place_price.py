# Generated by Django 4.2.3 on 2023-07-17 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_place_descrpition'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='price',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
