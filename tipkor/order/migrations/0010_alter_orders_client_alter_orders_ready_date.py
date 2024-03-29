# Generated by Django 4.0.5 on 2023-08-09 13:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_alter_orders_pay_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client_orders', to='order.clients'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='ready_date',
            field=models.DateTimeField(blank=True),
        ),
    ]
