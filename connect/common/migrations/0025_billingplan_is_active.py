# Generated by Django 3.2.9 on 2021-11-11 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0024_auto_20210826_1928'),
    ]

    operations = [
        migrations.AddField(
            model_name='billingplan',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='active plan'),
        ),
    ]
