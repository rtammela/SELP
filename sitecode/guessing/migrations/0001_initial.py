# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Matchchoice',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('winner_choice', models.CharField(max_length=200)),
                ('votes', models.IntegerField(default=0)),
                ('result', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Matchselect',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('match_info', models.CharField(max_length=200)),
                ('match_date', models.DateTimeField(verbose_name='date of match')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='matchchoice',
            name='match',
            field=models.ForeignKey(to='guessing.Matchselect'),
            preserve_default=True,
        ),
    ]
