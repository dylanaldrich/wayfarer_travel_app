# Generated by Django 3.1.2 on 2020-10-08 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.CharField(default='https://www.flaticon.com/svg/static/icons/svg/3288/3288532.svg', max_length=500),
        ),
    ]