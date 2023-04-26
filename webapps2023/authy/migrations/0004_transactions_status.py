# Generated by Django 4.1.7 on 2023-04-25 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authy', '0003_rename_description_transactions_remark'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactions',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending', max_length=20),
        ),
    ]
