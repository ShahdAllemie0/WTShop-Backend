# Generated by Django 3.1.2 on 2020-11-05 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0005_order_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='/media/profile.png', upload_to='profile_pic'),
        ),
    ]
