# Generated by Django 3.2.6 on 2021-08-11 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0034_auto_20210803_1931"),
    ]

    operations = [
        migrations.AddField(
            model_name="billingplan",
            name="card_expiration_date",
            field=models.CharField(
                blank=True, max_length=6, null=True, verbose_name="Card Expiration Date"
            ),
        ),
        migrations.AddField(
            model_name="billingplan",
            name="cardholder_name",
            field=models.TextField(
                blank=True, null=True, verbose_name="Cardholder Name"
            ),
        ),
        migrations.AddField(
            model_name="billingplan",
            name="final_card_number",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="Final Card Number"
            ),
        ),
    ]
