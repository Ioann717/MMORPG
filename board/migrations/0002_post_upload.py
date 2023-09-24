import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='upload',
            field=ckeditor_uploader.fields.RichTextUploadingField(default=1),
            preserve_default=False,
        ),
    ]
