# Generated by Django 2.2.12 on 2020-06-03 12:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='postroom',
            name='distance',
            field=models.FloatField(blank=True, null=True, verbose_name='거리 변수'),
        ),
        migrations.AlterField(
            model_name='postlike',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_query_name='postlikes', to='posts.PostRoom'),
        ),
    ]
