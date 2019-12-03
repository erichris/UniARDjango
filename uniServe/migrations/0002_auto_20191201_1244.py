# Generated by Django 2.2.6 on 2019-12-01 18:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uniServe.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('uniServe', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='uniar',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='files/'),
        ),
        migrations.AddField(
            model_name='uniar',
            name='fileBytes',
            field=models.BinaryField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='uniar',
            name='fileSize',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='uniar',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='uniar',
            name='imageBytes',
            field=models.BinaryField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='uniar',
            name='isPrivate',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='uniar',
            name='position_x',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='uniar',
            name='position_y',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='uniar',
            name='position_z',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='uniar',
            name='rotation_x',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='uniar',
            name='rotation_y',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='uniar',
            name='rotation_z',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='uniar',
            name='scale_x',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='uniar',
            name='scale_y',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='uniar',
            name='scale_z',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='uniar',
            name='uniFileType',
            field=models.IntegerField(blank=True, choices=[(uniServe.models.UniFileType(0), 0), (uniServe.models.UniFileType(1), 1), (uniServe.models.UniFileType(2), 2), (uniServe.models.UniFileType(3), 3)], null=True),
        ),
        migrations.AddField(
            model_name='uniar',
            name='uniHyperLink',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='uniar',
            name='uniType',
            field=models.IntegerField(blank=True, choices=[(uniServe.models.UniType(0), 0), (uniServe.models.UniType(1), 1), (uniServe.models.UniType(2), 2)], null=True),
        ),
        migrations.AlterField(
            model_name='uniar',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='uniar',
            name='uniCategory',
            field=models.IntegerField(blank=True, choices=[(uniServe.models.UniCategory(0), 0), (uniServe.models.UniCategory(1), 1), (uniServe.models.UniCategory(2), 2), (uniServe.models.UniCategory(3), 3), (uniServe.models.UniCategory(4), 4), (uniServe.models.UniCategory(5), 5)], null=True),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fbid', models.TextField(blank=True, max_length=500, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='uniar',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='uniServe.Profile'),
        ),
    ]
