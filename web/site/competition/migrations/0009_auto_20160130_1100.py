# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0008_remove_competition_judge_password'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='competition',
            options={'ordering': ['judge_date', 'name']},
        ),
        migrations.AddField(
            model_name='competition',
            name='type',
            field=models.CharField(default=b'ownpage', help_text=b'Whether entries are inline or on their own page', max_length=20, choices=[(b'simple', b'Simple'), (b'ownpage', b'Own Page')]),
        ),
    ]
