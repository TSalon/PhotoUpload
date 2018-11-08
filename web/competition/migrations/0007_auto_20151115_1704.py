# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0006_entry_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='position',
            field=models.IntegerField(help_text=b'The position of the image, last choice images will be dropped if too many entries', blank=True),
        ),
    ]
