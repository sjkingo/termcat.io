# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Paste',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('data', models.TextField()),
                ('remote_ip_addr', models.GenericIPAddressField()),
                ('created_dt', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Pastes',
                'verbose_name': 'Paste',
            },
        ),
    ]
