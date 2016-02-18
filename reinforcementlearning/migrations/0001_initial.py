# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GameBoard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
                ('grid_width', models.IntegerField()),
                ('grid_height', models.IntegerField()),
                ('start_x', models.IntegerField()),
                ('start_y', models.IntegerField()),
                ('goal_x', models.IntegerField()),
                ('goal_y', models.IntegerField()),
                ('death_coords', models.TextField()),
                ('number_of_episodes', models.IntegerField()),
                ('learning_rate', models.FloatField()),
                ('discount_rate', models.FloatField()),
                ('action_selection_parameter', models.FloatField()),
                ('success_rate', models.FloatField()),
                ('move_cost', models.FloatField()),
                ('death_cost', models.FloatField()),
                ('goal_reward', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
