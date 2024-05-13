# Generated by Django 2.1.15 on 2024-04-03 08:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HealthInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('checkup_date', models.DateField()),
                ('blood_pressure', models.CharField(max_length=20)),
                ('heart_disease', models.BooleanField(default=False)),
                ('smoking', models.BooleanField(default=False)),
                ('bmi', models.DecimalField(decimal_places=2, max_digits=5)),
                ('hba1c', models.DecimalField(decimal_places=2, max_digits=5)),
                ('blood_glucose', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='MedicalHistory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('result', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=100)),
                ('age', models.IntegerField()),
                ('gender', models.CharField(max_length=10)),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=15)),
            ],
        ),
        migrations.AddField(
            model_name='medicalhistory',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ungdung_app.Patient'),
        ),
        migrations.AddField(
            model_name='healthinfo',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ungdung_app.Patient'),
        ),
    ]