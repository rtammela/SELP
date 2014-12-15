# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Matchchoice',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('winner_choice', models.CharField(max_length=50)),
                ('votes', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Matchresult',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('winner', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Matchselect',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('game', models.CharField(max_length=200)),
                ('team1', models.CharField(max_length=50)),
                ('team2', models.CharField(max_length=50)),
                ('match_date', models.DateTimeField(verbose_name='date of match')),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Uservotes',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('match', models.ForeignKey(to='guessing.Matchselect')),
                ('voter', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('winner_choice', models.ForeignKey(to='guessing.Matchchoice')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='matchresult',
            name='match',
            field=models.ForeignKey(to='guessing.Matchselect'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='matchchoice',
            name='match',
            field=models.ForeignKey(to='guessing.Matchselect'),
            preserve_default=True,
        ),
    ]
