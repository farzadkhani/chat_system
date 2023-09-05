# Generated by Django 4.2.5 on 2023-09-05 09:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('communications', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_soft_deleted', models.BooleanField(default=False)),
                ('code', models.CharField(max_length=256)),
                ('is_read', models.BooleanField(default=False)),
                ('description', models.TextField()),
                ('message', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='communications.message')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
    ]
