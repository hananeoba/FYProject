# Generated by Django 5.0.2 on 2024-02-20 12:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basedataapp', '0002_initial'),
        ('userapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='basedataapp.company'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_role',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_structure',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='basedataapp.structure'),
        ),
    ]
