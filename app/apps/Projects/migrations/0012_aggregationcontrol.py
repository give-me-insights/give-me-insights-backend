# Generated by Django 4.1.4 on 2022-12-11 13:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Projects', '0011_alter_groupedsourcedata_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='AggregationControl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reset_process', models.BooleanField(default=False)),
                ('source', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Projects.datasource')),
            ],
        ),
    ]