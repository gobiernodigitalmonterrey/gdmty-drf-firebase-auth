# Generated by Django 4.2.2 on 2023-08-08 22:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FirebaseUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=191)),
            ],
        ),
        migrations.CreateModel(
            name='FirebaseUserProvider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=191)),
                ('provider_id', models.CharField(max_length=50)),
                ('firebase_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='provider', related_query_name='provider', to='gdmty_drf_firebase_auth.firebaseuser')),
            ],
        ),
    ]
