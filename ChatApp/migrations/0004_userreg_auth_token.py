# Generated by Django 5.1.1 on 2025-05-18 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ChatApp', '0003_userreg_is_set_auth'),
    ]

    operations = [
        migrations.AddField(
            model_name='userreg',
            name='auth_token',
            field=models.TextField(blank=True, null=True),
        ),
    ]
