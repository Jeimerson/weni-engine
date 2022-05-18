# Generated by Django 3.2.13 on 2022-05-18 19:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('common', '0050_project_flow_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='OpenedProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateTimeField(verbose_name='Day')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='opened_project', to='common.project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
