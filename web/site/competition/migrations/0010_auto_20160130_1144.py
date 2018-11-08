# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0009_auto_20160130_1100'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition',
            name='level',
            field=models.CharField(default=b'club', help_text=b'Level of competition', max_length=20, choices=[(b'club', b'Club Competition'), (b'clubwin', b'Club Print Winners'), (b'ypu', b'YPU Competition'), (b'pagb', b'PAGB Competition')]),
        ),
        migrations.AlterField(
            model_name='competition',
            name='type',
            field=models.CharField(default=b'ownpage', help_text=b'Whether entries are inline or on their own page', max_length=20, choices=[(b'inline', b'Inline'), (b'ownpage', b'Own Page')]),
        ),
    ]
