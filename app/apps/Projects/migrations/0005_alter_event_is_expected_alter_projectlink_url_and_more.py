# Generated by Django 4.1.4 on 2022-12-11 02:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Projects', '0004_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='is_expected',
            field=models.BooleanField(default=True, help_text='Info whether Event was expected or not (Corona 2019 would have been an unexpected event.)'),
        ),
        migrations.AlterField(
            model_name='projectlink',
            name='url',
            field=models.URLField(unique=True),
        ),
        migrations.CreateModel(
            name='SourceDataSchemaMapping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mapping', models.JSONField()),
                ('source', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='schema', to='Projects.datasource')),
            ],
        ),
    ]