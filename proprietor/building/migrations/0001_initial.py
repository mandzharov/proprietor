# Generated by Django 4.0.3 on 2022-04-09 20:00

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Apartment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('floor', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('number', models.CharField(max_length=10)),
                ('area', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('rooms_count', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('share', models.FloatField()),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=30)),
                ('street_address', models.CharField(max_length=60)),
                ('block_number', models.CharField(max_length=10)),
                ('postal_code', models.CharField(max_length=10)),
                ('floors_count', models.IntegerField()),
                ('alias', models.CharField(blank=True, max_length=30, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UtilityType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UtilitiesExpenses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6)),
                ('bill_year', models.IntegerField(choices=[(2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024), (2025, 2025), (2026, 2026), (2027, 2027), (2028, 2028), (2029, 2029), (2030, 2030), (2031, 2031), (2032, 2032), (2033, 2033), (2034, 2034), (2035, 2035), (2036, 2036), (2037, 2037), (2038, 2038), (2039, 2039), (2040, 2040), (2041, 2041), (2042, 2042), (2043, 2043), (2044, 2044), (2045, 2045), (2046, 2046), (2047, 2047), (2048, 2048), (2049, 2049), (2050, 2050), (2051, 2051), (2052, 2052), (2053, 2053), (2054, 2054), (2055, 2055), (2056, 2056), (2057, 2057), (2058, 2058), (2059, 2059), (2060, 2060), (2061, 2061), (2062, 2062), (2063, 2063), (2064, 2064), (2065, 2065), (2066, 2066), (2067, 2067), (2068, 2068), (2069, 2069), (2070, 2070), (2071, 2071), (2072, 2072), (2073, 2073), (2074, 2074), (2075, 2075), (2076, 2076), (2077, 2077), (2078, 2078), (2079, 2079), (2080, 2080), (2081, 2081), (2082, 2082), (2083, 2083), (2084, 2084), (2085, 2085), (2086, 2086), (2087, 2087), (2088, 2088), (2089, 2089), (2090, 2090), (2091, 2091), (2092, 2092), (2093, 2093), (2094, 2094), (2095, 2095), (2096, 2096), (2097, 2097), (2098, 2098)])),
                ('bill_month', models.CharField(blank=True, choices=[('JAN', 'January'), ('FEB', 'February'), ('MAR', 'March'), ('APR', 'April'), ('MAY', 'May'), ('JUN', 'Jun'), ('JUL', 'July'), ('AUG', 'August'), ('SEP', 'September'), ('OCT', 'October'), ('NOV', 'November'), ('DEC', 'December')], max_length=3, null=True)),
                ('entry_dt', models.DateTimeField(auto_now=True)),
                ('apartment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='building.apartment')),
                ('utility_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='building.utilitytype')),
            ],
        ),
        migrations.CreateModel(
            name='BuildingIncome',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6)),
                ('type', models.CharField(choices=[('Subscription', 'Subscription'), ('Rent', 'Rent'), ('Other', 'Other')], max_length=12)),
                ('description', models.TextField(blank=True, null=True)),
                ('deposit_date', models.DateField()),
                ('entry_dr', models.DateTimeField(auto_now_add=True)),
                ('apartment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='building.apartment')),
                ('building', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='building.building')),
            ],
        ),
        migrations.CreateModel(
            name='BuildingExpenses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6)),
                ('type', models.CharField(choices=[('Housekeeping', 'Housekeeping'), ('Planned', 'Planned'), ('Emergency', 'Emergency'), ('Salary', 'Salary'), ('Other', 'Other')], max_length=12)),
                ('description', models.TextField(blank=True, null=True)),
                ('payment_date', models.DateField()),
                ('entry_dr', models.DateTimeField(auto_now_add=True)),
                ('building', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='building.building')),
            ],
        ),
    ]
