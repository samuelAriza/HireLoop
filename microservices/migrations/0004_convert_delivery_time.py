from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('microservices', '0001_initial'),  # ajusta al último número de migración aplicado
    ]

    operations = [
        migrations.RunSQL(
            """
            ALTER TABLE microservices_microservice
            ALTER COLUMN delivery_time TYPE integer
            USING EXTRACT(EPOCH FROM delivery_time)::integer;
            """
        ),
    ]
