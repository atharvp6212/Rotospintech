# Generated by Django 3.1.1 on 2024-10-27 10:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_remove_subpart_colors'),
        ('orders', '0002_orderedsubpart_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderedsubpart',
            name='raw_material',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='inventory.rawmaterial'),
        ),
    ]
