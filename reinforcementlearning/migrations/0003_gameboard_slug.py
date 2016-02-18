# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('reinforcementlearning', '0002_gameboard_standard_set'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameboard',
            name='slug',
            field=models.SlugField(default=datetime.datetime(2015, 10, 2, 15, 44, 34, 970696, tzinfo=utc), unique=True),
            preserve_default=False,
        ),
    ]
