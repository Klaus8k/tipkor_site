# Generated by Django 4.0.5 on 2023-08-01 12:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stamp', '0003_alter_stamp_comment_alter_stamp_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stamp',
            name='file',
        ),
    ]
