# Generated by Django 3.2.3 on 2021-06-02 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0005_remove_post_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='likers',
            field=models.JSONField(default=[], verbose_name='likers'),
        ),
    ]
