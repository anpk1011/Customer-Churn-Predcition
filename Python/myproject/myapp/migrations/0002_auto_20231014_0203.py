# Generated by Django 4.2.6 on 2023-10-13 19:03

from django.db import migrations
import pandas as pd
df = pd.read_csv("E:\MyDemoOU\DoAN\Python\Churn_Modelling.csv")

def import_data(apps, schema_editor):
    # Import and insert your data here
    YourModel = apps.get_model('myapp', 'Customer')

    # Load data from your DataFrame (replace 'your_dataframe' with your actual DataFrame)
    data_to_import = df.to_dict(orient='records')

    for item in data_to_import:
        # Create a new object for YourModel with the data from the DataFrame
        YourModel.objects.create(**item)


class Migration(migrations.Migration):



    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(import_data),
    ]
