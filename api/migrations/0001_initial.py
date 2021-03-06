# Generated by Django 3.1.5 on 2021-01-20 12:29

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sync',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('requested', 'requested'), ('syncing', 'syncing'), ('done', 'done'), ('failed', 'failed')], default='syncing', max_length=64)),
                ('reason', models.CharField(blank=True, max_length=500, null=True)),
            ],
            options={
                'verbose_name': 'sync',
                'verbose_name_plural': 'syncs',
                'ordering': ['-created_date'],
            },
        ),
    ]
