# Generated by Django 4.1.4 on 2022-12-11 06:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Projects', '0006_alter_datasource_key_alter_event_key_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sourcedatarowraw',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Projects.datasource'),
        ),
    ]