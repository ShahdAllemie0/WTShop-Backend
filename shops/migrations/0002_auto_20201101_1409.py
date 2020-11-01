# Generated by Django 3.1.2 on 2020-11-01 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='order',
        ),
        migrations.AddField(
            model_name='cart',
            name='order',
            field=models.ManyToManyField(related_name='orderfffsC', to='shops.Order'),
        ),
        migrations.RemoveField(
            model_name='orderhistory',
            name='order',
        ),
        migrations.AddField(
            model_name='orderhistory',
            name='order',
            field=models.ManyToManyField(related_name='ordersSSS', to='shops.Order'),
        ),
    ]