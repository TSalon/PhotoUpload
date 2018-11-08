# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0010_auto_20160130_1144'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='competitor',
            options={'ordering': ['member_number']},
        ),
        migrations.AlterModelOptions(
            name='entry',
            options={'ordering': ['position']},
        ),
        migrations.RemoveField(
            model_name='competition',
            name='type',
        ),
        migrations.AlterField(
            model_name='competition',
            name='level',
            field=models.CharField(default=b'club', help_text=b'Type of competition', max_length=20, choices=[(b'club', b'Club Competition'), (b'external', b'External Competition')]),
        ),
    ]
