# Generated by Django 4.2.3 on 2023-07-11 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_place_filter'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='descrpition',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
    ]
