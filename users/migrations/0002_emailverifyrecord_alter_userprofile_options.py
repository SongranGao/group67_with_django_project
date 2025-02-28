# Generated by Django 5.1.5 on 2025-02-21 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailVerifyRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, verbose_name='verification code')),
                ('email', models.EmailField(max_length=35, verbose_name='email')),
                ('send_type', models.CharField(choices=[('register', 'register'), ('forget', 'retrieve password')], default='register', max_length=20)),
            ],
            options={
                'verbose_name': 'Email Verification Code',
                'verbose_name_plural': 'Email Verification Code',
            },
        ),
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': 'user data', 'verbose_name_plural': 'user data'},
        ),
    ]
