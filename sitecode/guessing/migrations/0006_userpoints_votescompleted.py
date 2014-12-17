# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('guessing', '0005_auto_20141217_1518'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpoints',
            name='votescompleted',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
