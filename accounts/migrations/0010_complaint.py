# Generated by Django 5.1.7 on 2025-03-22 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_rename_register_number_student_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('Hostel Facility', 'Hostel Facility'), ('Mess', 'Mess'), ('Students', 'Students'), ('Staff', 'Staff'), ('Others', 'Others')], max_length=50)),
                ('description', models.TextField()),
                ('file', models.FileField(blank=True, null=True, upload_to='complaints_files/')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
