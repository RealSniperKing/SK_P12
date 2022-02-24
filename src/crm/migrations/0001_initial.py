# Generated by Django 4.0.1 on 2022-02-11 13:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=200)),
                ('last_name', models.CharField(blank=True, max_length=200)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('phone', models.CharField(blank=True, max_length=12)),
                ('mobile', models.CharField(blank=True, max_length=12)),
                ('company_name', models.CharField(max_length=200)),
                ('address', models.CharField(blank=True, max_length=200)),
                ('address_complement', models.CharField(blank=True, max_length=200)),
                ('postal_code', models.CharField(blank=True, max_length=200)),
                ('city', models.CharField(blank=True, max_length=200)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updating_time', models.DateTimeField(null=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='author_user_id', to=settings.AUTH_USER_MODEL)),
                ('sales_contact', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='_sales_user_id', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
