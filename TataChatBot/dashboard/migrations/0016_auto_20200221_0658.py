# Generated by Django 2.0 on 2020-02-21 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0015_auto_20200221_0657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nodesmodule',
            name='parental_node_id',
            field=models.IntegerField(default=0),
        ),
    ]
