# Generated by Django 2.2 on 2020-04-27 09:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parsers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduledTimePoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField()),
                ('parser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parsers.Parser')),
            ],
        ),
    ]
