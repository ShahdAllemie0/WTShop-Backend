# Generated by Django 3.1.2 on 2020-11-04 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0004_remove_order_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=6, null=True),
        ),
    ]