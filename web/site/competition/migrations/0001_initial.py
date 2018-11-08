# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateField(help_text=b'Date the competition opens')),
                ('end_date', models.DateField(help_text=b'Last date for entries into the competition')),
                ('judge_date', models.DateField(help_text=b'The date that the competition will be judged')),
                ('name', models.CharField(help_text=b'Name of the competition', max_length=200)),
                ('description', models.TextField(help_text=b'Judging criteria for the competition')),
                ('min_photos', models.IntegerField(default=1, help_text=b'The minimum number of photos that can be entered for this competition')),
                ('max_photos', models.IntegerField(default=3, help_text=b'The maximum number of photos that can be entered for this competition')),
            ],
        ),
        migrations.CreateModel(
            name='Competitor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('surname', models.CharField(help_text=b'Competitor surname', max_length=50)),
                ('member_number', models.CharField(help_text=b'The icc unique member number', max_length=5)),
                ('last_upload', models.DateTimeField(help_text=b'The last time this person uploaded anything')),
                ('first_upload', models.DateTimeField(help_text=b'The first time this person uploaded anything')),
            ],
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('photo', models.ImageField(help_text=b'The photograph entered', upload_to=b'photos/%Y/%m/%d')),
                ('competition', models.ForeignKey(help_text=b'The competition this photograph is entered into', to='competition.Competition')),
                ('owner', models.ForeignKey(help_text=b'The person entering this competition', to='competition.Competitor')),
            ],
        ),
    ]
