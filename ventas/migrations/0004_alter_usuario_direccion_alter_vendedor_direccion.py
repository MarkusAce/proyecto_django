# Generated by Django 4.1.2 on 2024-06-28 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0003_vendedor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='direccion',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='vendedor',
            name='direccion',
            field=models.CharField(max_length=100),
        ),
    ]