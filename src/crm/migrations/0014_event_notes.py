# Generated by Django 4.0.1 on 2022-04-07 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0013_event_attendees'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='notes',
            field=models.CharField(max_length=1024, null=True),
        ),
    ]
