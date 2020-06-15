# Generated by Django 2.2 on 2020-04-28 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='slug',
            field=models.SlugField(default='dsadsa', unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='job',
            name='source',
            field=models.CharField(choices=[('angel', 'AngelList'), ('indeed', 'Indeed'), ('remoteok', 'RemoteOK')], max_length=100),
        ),
    ]
