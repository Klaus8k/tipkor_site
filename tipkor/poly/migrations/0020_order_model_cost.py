# Generated by Django 4.0.5 on 2023-06-13 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poly', '0019_alter_card_model_format_alter_leaflets_model_format'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_model',
            name='cost',
            field=models.IntegerField(null=True),
        ),
    ]
