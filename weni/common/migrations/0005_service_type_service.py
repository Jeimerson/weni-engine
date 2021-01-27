# Generated by Django 2.2.17 on 2021-01-22 19:07

from django.db import migrations, models


def noop(apps, schema_editor):  # pragma: no cover
    pass


def migrate(apps, schema_editor):  # pragma: no cover
    Service = apps.get_model("common", "Service")

    for service in Service.objects.all():
        if service.rocket_chat:
            service.type_service = "type_service_chat"
            service.save(update_fields=["type_service"])


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0004_auto_20210114_1405"),
    ]

    operations = [
        migrations.AddField(
            model_name="service",
            name="type_service",
            field=models.CharField(
                choices=[
                    ("type_service_flows", "Flows service"),
                    ("type_service_inteligence", "Inteligence Service"),
                    ("type_service_chat", "Chat Service"),
                ],
                default="type_service_chat",
                max_length=50,
                verbose_name="type service",
            ),
        ),
        migrations.RunPython(migrate, noop),
        migrations.RemoveField(
            model_name="service",
            name="rocket_chat",
        ),
    ]
