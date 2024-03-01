# Generated by Django 5.0.2 on 2024-03-01 12:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0002_user_groups_user_user_permissions'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=249, verbose_name='Order category name')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=249, verbose_name='Title')),
                ('info', models.TextField(verbose_name='Description')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('is_completed', models.BooleanField(default=False)),
                ('is_taken', models.BooleanField(default=False, verbose_name='Is taken')),
                ('taked_at', models.DateTimeField(blank=True, null=True)),
                ('squad', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='account.squad', verbose_name='Initiator')),
                ('volunter', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='account.volunter', verbose_name='Contractor')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.ordercategory')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Fundraising',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=249, verbose_name='Title')),
                ('info', models.TextField(verbose_name='Description')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('is_completed', models.BooleanField(default=False)),
                ('price', models.DecimalField(decimal_places=2, max_digits=9)),
                ('squad', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='account.squad', verbose_name='Initiator')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.ordercategory')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=9)),
                ('fundraising', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.fundraising')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
