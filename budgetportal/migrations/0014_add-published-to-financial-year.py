# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-02-20 16:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("budgetportal", "0013_add-department-website-name-ordering")]

    operations = [
        migrations.AlterModelOptions(
            name="financialyear", options={"ordering": ["-slug"]}
        ),
        migrations.AddField(
            model_name="financialyear",
            name="published",
            field=models.BooleanField(default=False),
        ),
    ]
