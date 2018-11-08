# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0002_auto_20151107_1528'),
    ]

    operations = [
        migrations.AddField(
            model_name='competitor',
            name='enabled',
            field=models.BooleanField(default=True, help_text=b'Whether this person is allowed to enter contests or not'),
        ),
    ]
