# Generated by Django 4.0.2 on 2022-03-13 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accountApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='confirmationtoken',
            name='token',
            field=models.CharField(max_length=128),
        ),
    ]