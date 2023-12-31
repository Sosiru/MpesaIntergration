# Generated by Django 4.2.4 on 2024-01-08 19:45

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
        ('billing', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientcredentials',
            name='state',
            field=models.ForeignKey(default=uuid.UUID('f116c446-8fa3-4c4f-b429-70095bc5e92d'), on_delete=django.db.models.deletion.CASCADE, to='base.state'),
        ),
        migrations.AlterField(
            model_name='paymenttransaction',
            name='state',
            field=models.ForeignKey(default=uuid.UUID('f116c446-8fa3-4c4f-b429-70095bc5e92d'), on_delete=django.db.models.deletion.CASCADE, to='base.state'),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='state',
            field=models.ForeignKey(default=uuid.UUID('f116c446-8fa3-4c4f-b429-70095bc5e92d'), on_delete=django.db.models.deletion.CASCADE, to='base.state'),
        ),
    ]
