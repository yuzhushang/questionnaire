# Generated by Django 2.0.7 on 2018-07-15 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fangdong', '0007_visitors_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitrecords',
            name='question7_score',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='visitrecords',
            name='question8_score',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='visitrecords',
            name='question1_score',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='visitrecords',
            name='question2_score',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='visitrecords',
            name='question3_score',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='visitrecords',
            name='question4_score',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='visitrecords',
            name='question5_score',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='visitrecords',
            name='question6_score',
            field=models.CharField(max_length=10, null=True),
        ),
    ]