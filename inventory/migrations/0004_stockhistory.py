# Generated by Django 3.1.1 on 2024-10-26 19:58

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_auto_20241019_0055'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('quantity_before', models.FloatField()),
                ('quantity_added', models.FloatField()),
                ('quantity_after', models.FloatField()),
                ('raw_material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stock_history', to='inventory.rawmaterial')),
            ],
        ),
    ]
