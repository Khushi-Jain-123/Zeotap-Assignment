# Generated by Django 5.0.6 on 2024-10-23 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rules", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Rule",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("rule_string", models.TextField()),
                ("ast", models.JSONField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(model_name="node", name="node_type",),
        migrations.AddField(
            model_name="node",
            name="type",
            field=models.CharField(default="operand", max_length=20),
        ),
        migrations.AlterField(
            model_name="node",
            name="value",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
