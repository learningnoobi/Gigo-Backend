# Generated by Django 4.1.3 on 2022-11-12 05:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("waste_system", "0003_alter_companycustomer_subscribed_date"),
        ("users", "0006_alter_user_subscribed_company"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="subscribed_company",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="waste_system.wastemanagementcompany",
            ),
        ),
    ]