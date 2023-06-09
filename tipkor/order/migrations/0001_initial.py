# Generated by Django 4.0.5 on 2023-06-21 17:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('tel', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField()),
                ('poduct', models.JSONField()),
                ('ready_date', models.DateField()),
                ('pay_info', models.BooleanField()),
                ('file', models.FileField(upload_to='')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='order.clients')),
            ],
        ),
    ]
