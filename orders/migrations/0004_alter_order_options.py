# Generated by Django 4.2.9 on 2024-04-05 13:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_order_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ('-id',), 'verbose_name': 'Order', 'verbose_name_plural': 'Orders'},
        ),
    ]
