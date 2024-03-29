# Generated by Django 4.0.10 on 2024-03-05 22:15

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('eventapp', '0002_initial'),
        ('basedataapp', '0005_rename_installation_id_work_installation_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ActivityNature',
            new_name='Activity_Nature',
        ),
        migrations.RenameModel(
            old_name='EventType',
            new_name='Event_Type',
        ),
        migrations.RenameModel(
            old_name='StructureType',
            new_name='Structure_Type',
        ),
        migrations.RenameModel(
            old_name='WorkType',
            new_name='Work_Type',
        ),
        migrations.RenameField(
            model_name='structure',
            old_name='structure_parent',
            new_name='parent_structure',
        ),
        migrations.AlterField(
            model_name='structure',
            name='province',
            field=models.ManyToManyField(related_name='province', to='basedataapp.province'),
        ),
    ]
