# Generated by Django 5.0.3 on 2024-06-06 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistemaSolit', '0017_usoproducto'),
    ]

    operations = [
        migrations.AddField(
            model_name='reparto',
            name='nombreCliente',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
