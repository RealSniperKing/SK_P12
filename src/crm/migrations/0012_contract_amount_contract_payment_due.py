# Generated by Django 4.0.1 on 2022-04-07 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0011_alter_contract_client'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='amount',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='contract',
            name='payment_due',
            field=models.DateTimeField(null=True),
        ),
    ]
