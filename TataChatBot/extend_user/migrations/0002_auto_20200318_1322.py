# Generated by Django 2.2 on 2020-03-18 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extend_user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='id',
            field=models.IntegerField(db_column='_id', primary_key=True, serialize=False),
        ),
    ]
