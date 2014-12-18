# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('guessing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uservotes',
            name='winner_choice',
            field=models.CharField(max_length=50),
            preserve_default=True,
        ),
    ]
