# Generated by Django 4.2.3 on 2023-08-20 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_place_avaliations_place_score_place_total_score_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='location',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='name',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
    ]