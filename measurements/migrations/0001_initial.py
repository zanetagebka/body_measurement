# Generated by Django 5.1.6 on 2025-03-07 19:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('weight', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('waist', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('hips', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('chest', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('thigh', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('calf', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('forearm', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]
