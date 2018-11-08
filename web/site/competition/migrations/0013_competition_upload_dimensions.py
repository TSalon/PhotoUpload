# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0012_auto_20161209_1037'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition',
            name='upload_dimensions',
            field=models.CharField(default=b'1050x1400', help_text=b'dimensions of PDI required', max_length=12, choices=[(b'1050x1400', b'1050 x 1400'), (b'1200x1600', b'1200 x 1600')]),
        ),
    ]
