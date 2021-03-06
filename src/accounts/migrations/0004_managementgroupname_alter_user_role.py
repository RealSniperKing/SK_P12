# Generated by Django 4.0.1 on 2022-03-03 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_user_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='ManagementGroupName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('Equipe de support', 'Equipe de support'), ('Equipe de gestion', 'Equipe de gestion'), ('Equipe de vente', 'Equipe de vente')], default='3', max_length=64),
        ),
    ]
