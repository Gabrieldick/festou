# Generated by Django 4.2.3 on 2023-07-07 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50)),
                ('Email', models.CharField(default='', max_length=50)),
                ('CPF', models.CharField(default='', max_length=50)),
                ('Celular', models.CharField(default='', max_length=50)),
                ('Senha', models.CharField(default='', max_length=50)),
                ('Data_de_aniversário', models.CharField(default='', max_length=50)),
                ('Banco', models.CharField(default='', max_length=50)),
                ('Conta', models.CharField(default='', max_length=50)),
                ('Agencia', models.CharField(default='', max_length=50)),
            ],
        ),
    ]