# Generated by Django 4.1.2 on 2024-06-29 23:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ventas', '0005_alter_usuario_email1_alter_vendedor_email1'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendedor',
            name='id_comuna',
        ),
        migrations.AlterField(
            model_name='compra',
            name='rut',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Usuario',
        ),
        migrations.DeleteModel(
            name='Vendedor',
        ),
    ]
