# Generated by Django 4.0.1 on 2022-04-07 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0012_contract_amount_contract_payment_due'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='attendees',
            field=models.IntegerField(null=True),
        ),
    ]