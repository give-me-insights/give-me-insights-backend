# Generated by Django 4.1.4 on 2022-12-10 18:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Projects', '0002_alter_project_unique_together_datasource'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datasource',
            name='key',
            field=models.CharField(editable=False, max_length=6, unique=True),
        ),
        migrations.AlterField(
            model_name='datasource',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Projects.project'),
        ),
        migrations.CreateModel(
            name='ProjectLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(editable=False, max_length=6, unique=True)),
                ('title', models.CharField(max_length=128)),
                ('description', models.TextField(blank=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('url', models.URLField()),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Projects.project')),
            ],
            options={
                'abstract': False,
                'unique_together': {('key', 'project')},
            },
        ),
    ]
