# Generated by Django 2.2.6 on 2019-12-01 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uniServe', '0005_auto_20191201_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='ProfileImages/'),
        ),
        migrations.AlterField(
            model_name='uniar',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='files/'),
        ),
        migrations.AlterField(
            model_name='uniar',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='images/'),
        ),
    ]
