# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_sequence_mixin.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mymodel',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('enabled', models.BooleanField()),
                ('num', models.IntegerField()),
            ],
            bases=(models.Model, django_sequence_mixin.models.SequenceMixin),
        ),
    ]
