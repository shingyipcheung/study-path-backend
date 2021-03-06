# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-08 03:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contribution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ratio', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='LearningObject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=40)),
                ('name', models.CharField(max_length=100)),
                ('max_score', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField()),
                ('time', models.DateTimeField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='edxDB.Question')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='record',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='edxDB.Student'),
        ),
        migrations.AddField(
            model_name='contribution',
            name='learning_object',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='edxDB.LearningObject'),
        ),
        migrations.AddField(
            model_name='contribution',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='edxDB.Question'),
        ),
    ]
