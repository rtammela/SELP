# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('guessing', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='matchchoice',
            name='result',
        ),
        migrations.AddField(
            model_name='matchselect',
            name='result',
            field=models.CharField(default='unknown', max_length=200),
            preserve_default=True,
        ),
    ]
