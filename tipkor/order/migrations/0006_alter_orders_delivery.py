# Generated by Django 4.0.5 on 2023-08-01 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_orders_comment_orders_delivery'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='delivery',
            field=models.CharField(blank=True, default='no', max_length=100),
        ),
    ]