# Generated by Django 4.1.4 on 2023-03-13 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profileimg',
            field=models.ImageField(default='blank_profile.png', upload_to='profile_images'),
        ),
    ]