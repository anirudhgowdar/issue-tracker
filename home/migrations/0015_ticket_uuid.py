# Generated by Django 3.1.3 on 2020-12-24 14:43

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_auto_20201224_1413'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
