# Generated by Django 4.0.5 on 2023-06-03 10:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('poly', '0008_alter_leaflets_x_alter_leaflets_y'),
    ]

    operations = [
        migrations.CreateModel(
            name='Leaflets_Model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x', models.IntegerField(blank=True, help_text='Горизонтальный размер', null=True)),
                ('y', models.IntegerField(blank=True, help_text='Вертикальный размер', null=True)),
                ('paper', models.CharField(choices=[('130', '130 г/м'), ('170', '170 г/м'), ('300', '300 г/м')], help_text='Плотность бумаги', max_length=20)),
                ('pressrun', models.IntegerField(help_text='Тираж')),
                ('duplex', models.BooleanField(choices=[(True, '4+4'), (False, '4+0')], default=True, help_text='Дуплекс')),
                ('cost', models.IntegerField(help_text='Цена', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RenameModel(
            old_name='Cards',
            new_name='Card_Model',
        ),
        migrations.RenameModel(
            old_name='FormatsPoly',
            new_name='Formats_Poly_Model',
        ),
        migrations.DeleteModel(
            name='Leaflets',
        ),
        migrations.AddField(
            model_name='leaflets_model',
            name='format_choice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poly.formats_poly_model'),
        ),
    ]