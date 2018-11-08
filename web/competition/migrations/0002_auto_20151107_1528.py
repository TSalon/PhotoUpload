# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='competitor',
            name='first_name',
            field=models.CharField(default='asdf', help_text=b'Competitor first name', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='competitor',
            name='first_upload',
            field=models.DateTimeField(help_text=b'The first time this person uploaded anything', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='competitor',
            name='last_upload',
            field=models.DateTimeField(help_text=b'The last time this person uploaded anything', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='competitor',
            name='surname',
            field=models.CharField(help_text=b'Competitor surname for login', max_length=50),
        ),
    ]
