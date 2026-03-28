from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_alter_sosrequest_emergency_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="age",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="name",
            field=models.CharField(blank=True, default="", max_length=200),
        ),
        migrations.CreateModel(
            name="EmergencyContact",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("phone", models.CharField(max_length=15)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="contacts", to="core.user")),
            ],
        ),
    ]
