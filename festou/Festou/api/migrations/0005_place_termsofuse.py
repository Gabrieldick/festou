# Generated by Django 4.2.4 on 2023-08-17 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_user_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='termsofuse',
            field=models.CharField(blank=True, max_length=8192, null=True),
        ),
    ]
