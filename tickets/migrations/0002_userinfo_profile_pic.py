# Generated by Django 3.0.8 on 2020-07-25 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='profile_pic',
            field=models.ImageField(blank=True, default='./profile_images/profile_pic1.png', null=True, upload_to='profile_images'),
        ),
    ]
