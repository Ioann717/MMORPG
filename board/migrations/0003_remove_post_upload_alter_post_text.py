import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_post_upload'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='upload',
        ),
        migrations.AlterField(
            model_name='post',
            name='text',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
