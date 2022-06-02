# Generated by Django 4.0.4 on 2022-05-26 13:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0009_auto_20220526_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table',
            name='cook',
            field=models.ForeignKey(limit_choices_to=models.Q(('groups__name', 'cooks'), ('is_superuser', True), _connector='OR'), null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='table', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='table',
            name='server',
            field=models.ForeignKey(limit_choices_to=models.Q(('groups__name', 'servers'), ('is_superuser', True), _connector='OR'), null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tables', to=settings.AUTH_USER_MODEL),
        ),
    ]