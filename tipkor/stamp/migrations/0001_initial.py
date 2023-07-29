# Generated by Django 4.0.5 on 2023-07-28 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stamp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_stamp', models.CharField(choices=[('c_stamp', 'печать'), ('r_stamp', 'штампа')], max_length=50)),
                ('express', models.BooleanField()),
                ('file', models.FileField(upload_to='')),
                ('comment', models.TextField(blank=True)),
                ('snap', models.CharField(choices=[('авто', 'авто'), ('обычная', 'обычная')], max_length=50)),
                ('count', models.IntegerField()),
                ('cost', models.IntegerField()),
            ],
        ),
    ]