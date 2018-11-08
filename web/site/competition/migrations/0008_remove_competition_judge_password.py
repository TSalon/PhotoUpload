# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0007_auto_20151115_1704'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='competition',
            name='judge_password',
        ),
    ]
