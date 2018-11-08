# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0004_auto_20151107_1606'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition',
            name='judge_password',
            field=models.CharField(default='fred', help_text=b'Unique password for the judge to prevent others seeing the pictures', max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='entry',
            name='photo',
            field=models.ImageField(help_text=b'Click "Choose File" to select your .JPG file to enter', upload_to=b'photos/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='title',
            field=models.CharField(help_text=b'A short title for your image', max_length=100),
        ),
    ]
