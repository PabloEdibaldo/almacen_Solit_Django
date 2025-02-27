# Generated by Django 5.0.3 on 2024-06-05 19:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistemaSolit', '0016_zonasalmacen_productos_zonaalmacen'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsoProducto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cliente', models.CharField(blank=True, max_length=250, null=True)),
                ('tipoUsio', models.CharField(blank=True, max_length=250, null=True)),
                ('productos', models.JSONField(blank=True, null=True)),
                ('fecha_uso', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
