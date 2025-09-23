# Generated manually to replace django-taggit with simple text field
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_fix_taggit_sqlite"),
    ]

    operations = [
        # Remove the taggit field and add a simple CharField
        migrations.RemoveField(
            model_name="freelancerprofile",
            name="skills",
        ),
        migrations.AddField(
            model_name="freelancerprofile",
            name="skills",
            field=models.CharField(
                blank=True,
                help_text="Enter skills separated by commas",
                max_length=500,
                verbose_name="Skills",
            ),
        ),
    ]
