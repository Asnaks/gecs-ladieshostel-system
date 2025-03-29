# Generated by Django 5.1.7 on 2025-03-29 00:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_remove_student_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessCommittee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.CharField(max_length=20)),
                ('year', models.IntegerField()),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.student')),
            ],
            options={
                'unique_together': {('student', 'month', 'year')},
            },
        ),
    ]
