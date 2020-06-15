# Generated by Django 2.2 on 2020-04-30 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_auto_20200428_1226'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='is_old',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='job',
            name='experience',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='skills',
            field=models.TextField(blank=True),
        ),
    ]