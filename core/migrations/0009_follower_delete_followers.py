# Generated by Django 4.1.4 on 2023-03-21 05:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_followers'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follower',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('following_user_id', models.ManyToManyField(blank=True, related_name='following', to='core.profile')),
                ('user_following', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='the_user', to='core.profile')),
            ],
        ),
        migrations.DeleteModel(
            name='Followers',
        ),
    ]
