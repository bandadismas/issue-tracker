# Generated by Django 3.0.8 on 2020-07-25 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0002_userinfo_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
