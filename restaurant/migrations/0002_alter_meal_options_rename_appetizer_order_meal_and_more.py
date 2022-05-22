# Generated by Django 4.0.4 on 2022-05-21 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='meal',
            options={'ordering': ['kind']},
        ),
        migrations.RenameField(
            model_name='order',
            old_name='appetizer',
            new_name='meal',
        ),
        migrations.AlterField(
            model_name='meal',
            name='kind',
            field=models.CharField(choices=[('appetizer', 'appetizer'), ('entree', 'entree'), ('side', 'side'), ('other', 'other'), ('rice', 'rice')], max_length=50),
        ),
    ]