# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0003_competitor_enabled'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='competition',
            options={'ordering': ['-judge_date', 'name']},
        ),
        migrations.AddField(
            model_name='entry',
            name='title',
            field=models.CharField(default='asdf', max_length=100),
            preserve_default=False,
        ),
    ]
