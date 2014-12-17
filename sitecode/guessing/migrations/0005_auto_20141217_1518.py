# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('guessing', '0004_userpoints_totalvotes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchselect',
            name='match_date',
            field=models.DateField(verbose_name='date of match'),
            preserve_default=True,
        ),
    ]
