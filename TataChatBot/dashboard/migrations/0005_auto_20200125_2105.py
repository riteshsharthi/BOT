# Generated by Django 2.2 on 2020-01-25 21:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_faq_use_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='faq',
            name='create_dt',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='faq',
            name='link',
            field=models.CharField(default='', max_length=200),
        ),
    ]