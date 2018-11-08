# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0005_auto_20151115_1616'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='position',
            field=models.IntegerField(default=1, help_text=b'The position of the image, last choice images will be dropped if too many entries'),
            preserve_default=False,
        ),
    ]
