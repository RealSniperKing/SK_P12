# Generated by Django 4.0.1 on 2022-02-10 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_user_groups_user_is_superuser_user_user_permissions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, choices=[('0', 'Management'), ('1', 'Sale'), ('2', 'Support'), ('3', 'Client')], max_length=64),
        ),
    ]
