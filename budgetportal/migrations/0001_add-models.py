# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-14 08:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Department",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("slug", models.SlugField(max_length=200, unique=True)),
                ("name", models.CharField(max_length=200, unique=True)),
                ("vote_number", models.IntegerField(unique=True)),
                ("intro", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="FinancialYear",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("slug", models.SlugField(max_length=7, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Government",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("slug", models.SlugField(max_length=200, unique=True)),
                ("name", models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Sphere",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("slug", models.SlugField(max_length=200, unique=True)),
                ("name", models.CharField(max_length=200, unique=True)),
                (
                    "financial_year",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="budgetportal.FinancialYear",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="government",
            name="sphere",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="budgetportal.Sphere"
            ),
        ),
        migrations.AddField(
            model_name="department",
            name="government",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="budgetportal.Government",
            ),
        ),
    ]
