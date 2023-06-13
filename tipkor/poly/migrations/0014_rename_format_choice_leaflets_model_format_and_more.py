# Generated by Django 4.0.5 on 2023-06-08 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poly', '0013_remove_order_model_order_card_model_type_production_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='leaflets_model',
            old_name='format_choice',
            new_name='format',
        ),
        migrations.RemoveField(
            model_name='card_model',
            name='type_production',
        ),
        migrations.RemoveField(
            model_name='card_model',
            name='x',
        ),
        migrations.RemoveField(
            model_name='card_model',
            name='y',
        ),
        migrations.RemoveField(
            model_name='leaflets_model',
            name='x',
        ),
        migrations.RemoveField(
            model_name='leaflets_model',
            name='y',
        ),
        migrations.AddField(
            model_name='card_model',
            name='format',
            field=models.CharField(choices=[('90x50', '90x50мм')], max_length=20, null=True),
        ),
    ]