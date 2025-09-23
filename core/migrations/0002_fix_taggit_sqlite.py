# Generated manually to fix SQLite issues with django-taggit
from django.db import migrations, connection


def fix_taggit_sqlite_issue(apps, schema_editor):
    """
    Fix SQLite integer overflow issue with django-taggit.
    This resets the auto-increment counters that might be causing the issue.
    """
    if connection.vendor == "sqlite":
        with connection.cursor() as cursor:
            try:
                # Reset the sqlite_sequence table for taggit tables
                cursor.execute("DELETE FROM sqlite_sequence WHERE name LIKE 'taggit_%'")
                cursor.execute(
                    "DELETE FROM sqlite_sequence WHERE name = 'core_freelancerprofile_skills'"
                )
                print("DEBUG - Fixed SQLite sequence issue for taggit")
            except Exception as e:
                print(f"DEBUG - Could not fix SQLite sequence: {e}")


def reverse_fix(apps, schema_editor):
    # Nothing to reverse
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(fix_taggit_sqlite_issue, reverse_fix),
    ]
