# Generated by Django 4.1.4 on 2023-03-13 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_profile_firstname_profile_lastname'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='mobileNumber',
            field=models.BigIntegerField(null=True),
        ),
    ]
