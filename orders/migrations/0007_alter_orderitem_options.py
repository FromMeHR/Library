# Generated by Django 4.2.9 on 2024-04-13 16:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_alter_order_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderitem',
            options={'ordering': ('-id',), 'verbose_name': 'Ordered item', 'verbose_name_plural': 'Ordered items'},
        ),
    ]