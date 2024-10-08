# Generated by Django 5.1.1 on 2024-09-11 09:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tenders', '0004_alter_tender_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=500)),
                ('status', models.CharField(choices=[('Created', 'Created'), ('Published', 'Published'), ('Canceled', 'Canceled')])),
                ('authorType', models.CharField(choices=[('Organization', 'Organization'), ('User', 'User')])),
                ('version', models.IntegerField(db_default=1, default=1)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('authorId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.user')),
                ('tenderId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tenders.tender')),
            ],
        ),
    ]
