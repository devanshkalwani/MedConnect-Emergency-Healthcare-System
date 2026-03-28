from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_user_age_contact_and_name_update"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="pref_contact",
            field=models.CharField(blank=True, default="", max_length=100),
        ),
        migrations.AddField(
            model_name="user",
            name="pref_hospital",
            field=models.CharField(blank=True, default="", max_length=150),
        ),
    ]
