# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-08-16 14:35
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("budgetportal", "0028_video_videolanguage")]

    operations = [
        migrations.AlterModelOptions(
            name="event", options={"ordering": ["start_date"]}
        ),
        migrations.AlterModelOptions(
            name="videolanguage", options={"ordering": ["id"]}
        ),
        migrations.AddField(
            model_name="event",
            name="start_date",
            field=models.DateField(
                default=datetime.datetime(2019, 8, 16, 14, 35, 39, 966766)
            ),
        ),
    ]
