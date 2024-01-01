# Generated by Django 4.2.4 on 2024-01-01 11:26

import base.models
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('synced', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=50)),
                ('identifier', models.CharField(max_length=50, unique=True)),
                ('phone_number', models.CharField(blank=True, max_length=50, null=True)),
                ('email_address', models.CharField(blank=True, max_length=50, null=True)),
                ('address', models.CharField(blank=True, max_length=50, null=True)),
                ('postal_code', models.CharField(blank=True, max_length=50, null=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.country')),
                ('state', models.ForeignKey(default=base.models.State.default_state, on_delete=django.db.models.deletion.CASCADE, to='base.state')),
            ],
            options={
                'verbose_name_plural': 'Customer',
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('synced', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, max_length=255, null=True)),
                ('service_id', models.CharField(max_length=100, unique=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=25, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customer')),
                ('state', models.ForeignKey(default=base.models.State.default_state, on_delete=django.db.models.deletion.CASCADE, to='base.state')),
            ],
            options={
                'verbose_name_plural': 'Service',
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='CustomerAccount',
            fields=[
                ('synced', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('account_number', models.CharField(default=1000000000, max_length=50)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customer')),
                ('state', models.ForeignKey(default=base.models.State.default_state, on_delete=django.db.models.deletion.CASCADE, to='base.state')),
            ],
            options={
                'verbose_name_plural': 'Customer Account',
                'ordering': ['-date_created'],
            },
        ),
    ]
