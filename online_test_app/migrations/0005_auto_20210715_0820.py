# Generated by Django 3.2.5 on 2021-07-15 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_test_app', '0004_answermodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='answermodel',
            name='qNum',
            field=models.IntegerField(blank=True, default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='answermodel',
            name='answer',
            field=models.CharField(blank=True, max_length=6),
        ),
    ]
