from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0002_school_credentials'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='location',

            field=models.CharField(default='12.3052032,76.6222336', max_length=100),
        ),
    ]
