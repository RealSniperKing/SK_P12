# Generated by Django 4.0.1 on 2022-02-24 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0004_contract_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]