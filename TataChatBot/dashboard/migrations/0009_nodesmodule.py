# Generated by Django 2.0 on 2020-02-19 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_faq_create_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='NodesModule',
            fields=[
                ('id', models.IntegerField(db_column='_id', primary_key=True, serialize=False)),
                ('node_name', models.CharField(default='', max_length=70)),
                ('node_level', models.IntegerField(default=1)),
                ('parental_node', models.CharField(default='', max_length=70)),
                ('parental_node_level', models.IntegerField(default=1)),
            ],
        ),
    ]
