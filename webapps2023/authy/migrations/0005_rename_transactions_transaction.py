# Generated by Django 4.1.7 on 2023-04-25 04:50

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('authy', '0004_transactions_status'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Transactions',
            new_name='Transaction',
        ),
    ]
