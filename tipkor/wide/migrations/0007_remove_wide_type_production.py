# Generated by Django 4.0.5 on 2023-08-05 11:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wide', '0006_alter_material_type_material_alter_wide_heigth_size_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wide',
            name='type_production',
        ),
    ]