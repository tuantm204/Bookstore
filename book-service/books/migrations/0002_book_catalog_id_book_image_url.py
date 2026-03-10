# Generated migration for catalog_id and image_url fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='catalog_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='image_url',
            field=models.URLField(blank=True, default='', max_length=500),
        ),
    ]
