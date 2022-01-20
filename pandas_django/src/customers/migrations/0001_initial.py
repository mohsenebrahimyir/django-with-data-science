# Generated by Django 3.2 on 2022-01-20 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=220)),
                ('budget', models.PositiveIntegerField()),
                ('employment', models.PositiveIntegerField()),
                ('joined', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
