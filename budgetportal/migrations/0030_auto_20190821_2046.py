# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-08-21 20:46
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("budgetportal", "0029_auto_20190816_1435")]

    operations = [
        migrations.AlterModelOptions(
            name="event", options={"ordering": ["-start_date"]}
        ),
        migrations.AlterField(
            model_name="event",
            name="start_date",
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]
