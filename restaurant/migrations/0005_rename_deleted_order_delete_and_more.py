# Generated by Django 4.0.4 on 2022-05-24 14:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0004_alter_order_options_order_deleted_table_deleted_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='deleted',
            new_name='delete',
        ),
        migrations.RenameField(
            model_name='table',
            old_name='deleted',
            new_name='delete',
        ),
    ]