# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reinforcementlearning', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameboard',
            name='standard_set',
            field=models.NullBooleanField(),
            preserve_default=True,
        ),
    ]
