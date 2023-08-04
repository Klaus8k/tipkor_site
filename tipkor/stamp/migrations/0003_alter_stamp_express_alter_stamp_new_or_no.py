# Generated by Django 4.0.5 on 2023-08-03 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stamp', '0002_alter_stamp_new_or_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stamp',
            name='express',
            field=models.BooleanField(choices=[(True, 'Срочно'), (False, 'Стандарт')], default=False),
        ),
        migrations.AlterField(
            model_name='stamp',
            name='new_or_no',
            field=models.CharField(choices=[('new', 'Новая'), ('repeat', 'По оттиску')], default='new', max_length=20),
        ),
    ]