# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-14 08:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("budgetportal", "0001_add-models")]

    operations = [
        migrations.AlterField(
            model_name="sphere",
            name="financial_year",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="spheres",
                to="budgetportal.FinancialYear",
            ),
        )
    ]
