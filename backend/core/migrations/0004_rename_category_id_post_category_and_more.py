# Generated by Django 4.1.7 on 2023-03-07 12:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_rename_category_post_category_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='category_id',
            new_name='category',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='image_id',
            new_name='image',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='user_id',
            new_name='user',
        ),
    ]
