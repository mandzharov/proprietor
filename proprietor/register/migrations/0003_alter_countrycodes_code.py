# Generated by Django 4.0.3 on 2022-04-12 20:25

from django.db import migrations, models
import proprietor.register.models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0002_alter_profile_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='countrycodes',
            name='code',
            field=models.CharField(max_length=6, validators=[proprietor.register.models.country_code_validator]),
        ),
    ]
