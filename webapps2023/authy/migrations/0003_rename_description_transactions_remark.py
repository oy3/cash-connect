# Generated by Django 4.1.7 on 2023-04-24 23:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authy', '0002_transactions'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transactions',
            old_name='description',
            new_name='remark',
        ),
    ]
